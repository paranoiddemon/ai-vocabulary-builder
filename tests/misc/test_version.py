from voc_builder.misc.version import JohnnyDist


def test__JohnnyDist():
    _ = JohnnyDist(
        "ai-vocabulary-builder", index_urls=["https://piglei.com/"]
    ).versions_available()
