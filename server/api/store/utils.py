def create_seo_description(description: str) -> str:
    """
    Create short description for SEO from full product description.

    Full description will be sliced by `NUM_CHARACTERS` and split by first period `.`
    Text before period will be used as SEO description.

    Example:
        Ullamco officia esse esse consectetur dolore elit qui non eu sint proident.
        Irure elit irure ullamco aute aliqua et minim deserunt et nisi ut nostrud ullamco deserunt. Do ipsum sit tempor ullamco irure ipsum culpa dolore est.
        Commodo eu amet commodo culpa exercitation.
        Mollit sit deserunt dolore in ipsum consectetur magna eiusmod.

        will be sliced by first `NUM_CHARACTERS` then split by first period `.`

        Result:
            Ullamco officia esse esse consectetur dolore elit qui non eu sint proident
    """
    NUM_CHARACTERS = 150
    return description[:NUM_CHARACTERS].split(".")[0]
