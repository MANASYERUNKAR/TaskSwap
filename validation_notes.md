# TaskSwap Validation Notes

The exposed Django development server was checked in a browser after allowing the sandbox preview hostname in `ALLOWED_HOSTS`. The homepage returned normally with the title **“TaskSwap — Neighbours help neighbours”**. The rendered page included the TaskSwap brand navigation, the “Make the ask.” hero, the three full-height “Post it / Get help / Done” sections, the searchable and filterable task shelf, and the empty-state call to action.

The viewport render confirmed the intended Quiet Utility visual direction: a near-white surface, oversized dark system headline, compact navigation, restrained black pill CTA, and substantial negative space.

The server-side suite was also run successfully using `python3 manage.py test core -v 2`; all six integration tests passed.
