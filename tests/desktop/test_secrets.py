import pytest

from ws_tracker.desktop.bus import DBusCallError
from ws_tracker.desktop.secrets import SecretServiceStore, SecretsLocked, SecretsUnavailable

from .fakes import FakeBus

ROOT = "/org/freedesktop/secrets"
SVC = "org.freedesktop.Secret.Service"
COLL = "org.freedesktop.Secret.Collection"
ITEM = "org.freedesktop.Secret.Item"
PROMPT = "org.freedesktop.Secret.Prompt"
PROPS = "org.freedesktop.DBus.Properties"
COLLECTION = "/org/freedesktop/secrets/collection/kdewallet"
SESSION = "/org/freedesktop/secrets/session/1"


def wallet(*, items=("/item/1",), locked_items=(), locked_collection=False, secret=b"kimai-token"):
    bus = FakeBus()
    bus.on(ROOT, SVC, "OpenSession", (("s", ""), SESSION))
    bus.on(ROOT, SVC, "ReadAlias", (COLLECTION,))
    bus.on(COLLECTION, PROPS, "Get", (("b", locked_collection),))
    bus.on(ROOT, SVC, "SearchItems", (list(items), list(locked_items)))
    bus.on(
        ROOT,
        SVC,
        "GetSecrets",
        lambda body: ({path: (SESSION, b"", secret, "text/plain") for path in body[0]},),
    )
    bus.on(COLLECTION, COLL, "CreateItem", (f"{COLLECTION}/9", "/"))
    for path in (*items, *locked_items):
        bus.on(path, ITEM, "Delete", ("/",))
    return bus


def test_set_creates_an_item_with_label_attributes_and_secret():
    bus = wallet()
    SecretServiceStore(bus).set("https://kimai.firma.pl/", "  kimai-token  ")
    create = next(call for call in bus.calls if call[3] == "CreateItem")
    properties, secret, replace = create[5]
    assert properties["org.freedesktop.Secret.Item.Label"] == (
        "s",
        "WS Tracker — https://kimai.firma.pl",
    )
    assert properties["org.freedesktop.Secret.Item.Attributes"] == (
        "a{ss}",
        {"application": "io.github.dragonking026.WS-Tracker-Linux", "url": "https://kimai.firma.pl"},
    )
    assert secret == (SESSION, b"", b"kimai-token", "text/plain")
    assert replace is True
    assert create[4] == "a{sv}(oayays)b"


def test_get_returns_the_token_or_none():
    assert SecretServiceStore(wallet()).get("https://kimai.firma.pl") == "kimai-token"
    assert SecretServiceStore(wallet(items=())).get("https://kimai.firma.pl") is None


def test_session_is_opened_once():
    bus = wallet()
    store = SecretServiceStore(bus)
    store.get("https://a.test")
    store.get("https://a.test")
    assert bus.members().count("OpenSession") == 1


def test_delete_removes_every_match():
    bus = wallet(items=("/item/1", "/item/2"))
    SecretServiceStore(bus).delete("https://kimai.firma.pl")
    assert [call[1] for call in bus.calls if call[3] == "Delete"] == ["/item/1", "/item/2"]


def test_locked_item_is_unlocked_through_the_prompt():
    bus = wallet(items=(), locked_items=("/item/7",))
    bus.on(ROOT, SVC, "Unlock", ([], "/prompt/1"))
    bus.on("/prompt/1", PROMPT, "Prompt", ())
    bus.emit("/prompt/1", PROMPT, "Completed", (False, ("ao", ["/item/7"])))
    assert SecretServiceStore(bus).get("https://kimai.firma.pl") == "kimai-token"
    assert "Prompt" in bus.members()


def test_dismissed_unlock_prompt_is_locked():
    bus = wallet(items=(), locked_items=("/item/7",))
    bus.on(ROOT, SVC, "Unlock", ([], "/prompt/1"))
    bus.on("/prompt/1", PROMPT, "Prompt", ())
    bus.emit("/prompt/1", PROMPT, "Completed", (True, ("s", "")))
    with pytest.raises(SecretsLocked) as caught:
        SecretServiceStore(bus).get("https://kimai.firma.pl")
    assert "kimai-token" not in str(caught.value)


def test_locked_collection_is_unlocked_before_writing():
    bus = wallet(locked_collection=True)
    bus.on(ROOT, SVC, "Unlock", ([COLLECTION], "/"))
    SecretServiceStore(bus).set("https://kimai.firma.pl", "t")
    assert bus.members().index("Unlock") < bus.members().index("CreateItem")


@pytest.mark.parametrize(
    "name",
    [
        "org.freedesktop.DBus.Error.ServiceUnknown",
        "org.freedesktop.DBus.Error.AccessDenied",
        "org.freedesktop.DBus.Error.NameHasNoOwner",
    ],
)
def test_missing_service_is_unavailable(name):
    bus = FakeBus()
    bus.on(ROOT, SVC, "SearchItems", DBusCallError(name, "sandbox"))
    bus.on(ROOT, SVC, "OpenSession", DBusCallError(name, "sandbox"))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).get("https://kimai.firma.pl")


def test_no_default_collection_is_unavailable():
    bus = wallet()
    bus.on(ROOT, SVC, "ReadAlias", ("/",))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).set("https://kimai.firma.pl", "t")


def test_token_never_appears_in_errors():
    bus = wallet()
    bus.on(COLLECTION, COLL, "CreateItem", DBusCallError("org.freedesktop.DBus.Error.AccessDenied", "denied"))
    with pytest.raises(SecretsUnavailable) as caught:
        SecretServiceStore(bus).set("https://kimai.firma.pl", "super-secret-token")
    assert "super-secret-token" not in str(caught.value)


@pytest.mark.parametrize("error", [TimeoutError("no reply"), ConnectionResetError("bus closed")])
def test_hanging_or_closed_service_is_unavailable(error):
    bus = wallet()
    bus.on(ROOT, SVC, "SearchItems", error)
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).get("https://kimai.firma.pl")


def test_service_that_fails_to_start_is_unavailable():
    bus = wallet()
    bus.on(ROOT, SVC, "SearchItems", DBusCallError("org.freedesktop.DBus.Error.Spawn.ChildExited", "exit 1"))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).get("https://kimai.firma.pl")


@pytest.mark.parametrize(
    "name", ["org.freedesktop.Secret.Error.NoSession", "org.freedesktop.DBus.Error.UnknownObject"]
)
def test_stale_session_is_reopened_once(name):
    """After the secret service restarts, the cached session path is gone."""
    bus = wallet()
    store = SecretServiceStore(bus)
    assert store.get("https://kimai.firma.pl") == "kimai-token"
    answers = [DBusCallError(name, "gone")]

    def get_secrets(body):
        if answers:
            raise answers.pop()
        return ({path: (SESSION, b"", b"kimai-token", "text/plain") for path in body[0]},)

    bus.on(ROOT, SVC, "GetSecrets", get_secrets)
    assert store.get("https://kimai.firma.pl") == "kimai-token"
    assert bus.members().count("OpenSession") == 2


def test_session_that_stays_broken_is_unavailable():
    bus = wallet()
    bus.on(COLLECTION, COLL, "CreateItem", DBusCallError("org.freedesktop.Secret.Error.NoSession", "gone"))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).set("https://kimai.firma.pl", "t")


def test_get_reads_only_the_first_of_several_matches():
    bus = wallet(items=("/item/1", "/item/2"))
    assert SecretServiceStore(bus).get("https://kimai.firma.pl") == "kimai-token"
    get_secrets = next(call for call in bus.calls if call[3] == "GetSecrets")
    assert get_secrets[5][0] == ["/item/1"]


def test_item_gone_between_search_and_read_is_no_token():
    bus = wallet()
    bus.on(ROOT, SVC, "GetSecrets", ({},))
    assert SecretServiceStore(bus).get("https://kimai.firma.pl") is None


def test_secret_that_is_not_text_is_no_token():
    assert SecretServiceStore(wallet(secret=b"\xff\xfe")).get("https://kimai.firma.pl") is None


def test_unanswered_unlock_prompt_is_dismissed():
    bus = wallet(items=(), locked_items=("/item/7",))
    bus.on(ROOT, SVC, "Unlock", ([], "/prompt/1"))
    bus.on("/prompt/1", PROMPT, "Prompt", ())
    bus.on("/prompt/1", PROMPT, "Dismiss", ())
    with pytest.raises(SecretsLocked):
        SecretServiceStore(bus, prompt_timeout=0.01).get("https://kimai.firma.pl")
    assert bus.members()[-1] == "Dismiss"


def test_missing_service_when_saving_is_unavailable():
    bus = FakeBus()
    bus.on(ROOT, SVC, "ReadAlias", DBusCallError("org.freedesktop.DBus.Error.ServiceUnknown", "sandbox"))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).set("https://kimai.firma.pl", "t")
