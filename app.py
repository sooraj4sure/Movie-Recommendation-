import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-dvr3.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================
# STYLES — Cinematic Dark Theme
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,300&display=swap');

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #08090d !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(220,60,30,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 90% 80%, rgba(255,140,0,0.07) 0%, transparent 60%),
        #08090d !important;
}

[data-testid="stSidebar"] { display: none !important; }

[data-testid="stHeader"],
[data-testid="stToolbar"],
footer { display: none !important; }

.block-container {
    padding: 2rem 3rem !important;
    max-width: 1440px !important;
}

/* ── Hide Streamlit default UI chrome ── */
#MainMenu { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #dc3c1e; border-radius: 3px; }

/* ── HEADER ── */
.site-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0 2.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 2.5rem;
}
.site-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #ff6b35, #dc3c1e, #ff9a00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.site-tagline {
    color: rgba(232,230,225,0.4);
    font-size: 0.85rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── SEARCH BOX ── */
.search-wrap {
    position: relative;
    max-width: 680px;
    margin: 0 auto 2rem;
}
.search-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.12em;
    color: rgba(232,230,225,0.5);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1.4rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #dc3c1e !important;
    box-shadow: 0 0 0 3px rgba(220,60,30,0.18) !important;
    outline: none !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder { color: rgba(232,230,225,0.28) !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── SUGGESTIONS (pill chips, not dropdown) ── */
.suggestions-label {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(232,230,225,0.35);
    margin-bottom: 0.55rem;
    font-weight: 600;
}
.suggestions-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;
}
.suggestion-chip {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 0.38rem 1rem;
    font-size: 0.85rem;
    color: #e8e6e1;
    cursor: pointer;
    transition: background 0.18s, border-color 0.18s, transform 0.12s;
    white-space: nowrap;
}
.suggestion-chip:hover {
    background: rgba(220,60,30,0.2);
    border-color: #dc3c1e;
    transform: translateY(-1px);
}

/* ── SECTION HEADINGS ── */
.section-heading {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.08em;
    color: #e8e6e1;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-heading span.accent { color: #dc3c1e; }

/* ── CATEGORY PILLS (home feed) ── */
.cat-strip {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.cat-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 999px;
    padding: 0.45rem 1.15rem;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: rgba(232,230,225,0.65);
    cursor: pointer;
    transition: all 0.18s;
}
.cat-pill.active, .cat-pill:hover {
    background: rgba(220,60,30,0.22);
    border-color: #dc3c1e;
    color: #ff6b35;
}

/* ── MOVIE CARD ── */
.movie-card-wrap {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    transition: transform 0.22s, box-shadow 0.22s;
    cursor: pointer;
}
.movie-card-wrap:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.55), 0 0 0 1px rgba(220,60,30,0.3);
}
.movie-card-wrap img {
    width: 100%;
    display: block;
    border-radius: 14px 14px 0 0;
}
.movie-card-info {
    padding: 0.65rem 0.8rem 0.75rem;
    background: rgba(8,9,13,0.9);
}
.movie-card-title {
    font-size: 0.83rem;
    font-weight: 600;
    color: #e8e6e1;
    line-height: 1.25rem;
    max-height: 2.5rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.no-poster-box {
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.03);
    border-radius: 14px 14px 0 0;
    font-size: 2.5rem;
    color: rgba(255,255,255,0.15);
}

/* ── OPEN BUTTON ── */
.stButton > button {
    width: 100% !important;
    background: rgba(220,60,30,0.12) !important;
    border: 1px solid rgba(220,60,30,0.35) !important;
    border-radius: 8px !important;
    color: #ff6b35 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    padding: 0.35rem 0 !important;
    text-transform: uppercase !important;
    transition: background 0.18s, border-color 0.18s !important;
    margin-top: 0.4rem !important;
}
.stButton > button:hover {
    background: rgba(220,60,30,0.28) !important;
    border-color: #dc3c1e !important;
    color: #fff !important;
}

/* ── SELECTBOX (for category) hide completely when not needed ── */
[data-testid="stSelectbox"] { display: none !important; }

/* ── DETAILS PAGE ── */
.detail-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
}
.detail-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.04em;
    line-height: 1.05;
    color: #e8e6e1;
    margin-bottom: 0.5rem;
}
.detail-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.2rem;
}
.detail-badge {
    background: rgba(220,60,30,0.15);
    border: 1px solid rgba(220,60,30,0.3);
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #ff6b35;
    letter-spacing: 0.04em;
}
.detail-overview {
    font-size: 0.95rem;
    line-height: 1.75;
    color: rgba(232,230,225,0.75);
    font-weight: 300;
}
.back-btn-wrap .stButton > button {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: rgba(232,230,225,0.7) !important;
    border-radius: 999px !important;
    padding: 0.45rem 1.2rem !important;
    width: auto !important;
    font-size: 0.82rem !important;
}
.back-btn-wrap .stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    color: #fff !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 1.5rem 0 !important;
}

/* ── INFO / WARNING / ERROR ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e6e1 !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] > div { border-top-color: #dc3c1e !important; }

/* ── Streamlit image ── */
[data-testid="stImage"] img { border-radius: 14px; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "home_category" not in st.session_state:
    st.session_state.home_category = "trending"

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# POSTER GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div class='no-poster-box'>🎬</div>",
                        unsafe_allow_html=True,
                    )

                if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-card-title'>{title}</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)


# =============================
# SITE HEADER
# =============================
st.markdown(
    """
<div class="site-header">
    <div>
        <div class="site-logo">🎬 CineMatch</div>
        <div class="site-tagline">Discover your next obsession</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =============================
# VIEW: HOME
# =============================
if st.session_state.view == "home":

    # ── Search input (centered) ──
    _, mid, _ = st.columns([1, 2.5, 1])
    with mid:
        st.markdown("<div class='search-label'>🔍 Search Movies</div>", unsafe_allow_html=True)
        typed = st.text_input(
            "search",
            placeholder="avengers, batman, love story...",
            label_visibility="collapsed",
        )

    # ── Search mode ──
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching…"):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                # ── Inline suggestion chips (NOT dropdown) ──
                if suggestions:
                    _, mid2, _ = st.columns([1, 2.5, 1])
                    with mid2:
                        st.markdown(
                            "<div class='suggestions-label'>You Might Also Like </div>",
                            unsafe_allow_html=True,
                        )
                        # Render chips as buttons in a horizontal layout
                        num_chips = len(suggestions)
                        chip_cols = st.columns(min(num_chips, 5))
                        for i, (label, tmdb_id) in enumerate(suggestions[:5]):
                            with chip_cols[i % min(num_chips, 5)]:
                                if st.button(
                                    label,
                                    key=f"chip_{i}_{tmdb_id}",
                                    use_container_width=True,
                                ):
                                    goto_details(tmdb_id)

                        # Second row for remaining chips
                        remaining = suggestions[5:]
                        if remaining:
                            chip_cols2 = st.columns(min(len(remaining), 5))
                            for i, (label, tmdb_id) in enumerate(remaining):
                                with chip_cols2[i % min(len(remaining), 5)]:
                                    if st.button(
                                        label,
                                        key=f"chip2_{i}_{tmdb_id}",
                                        use_container_width=True,
                                    ):
                                        goto_details(tmdb_id)

                st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='section-heading'>Results <span class='accent'>_</span></div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=6, key_prefix="search_results")

        st.stop()

    # ── Home feed category selector ──
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    categories = ["trending", "popular", "top_rated", "now_playing", "upcoming"]
    cat_labels  = ["🔥 Trending", "⭐ Popular", "🏆 Top Rated", "▶ Now Playing", "🗓 Upcoming"]

    # Render category pills as buttons
    cat_cols = st.columns(len(categories))
    for i, (cat, label) in enumerate(zip(categories, cat_labels)):
        with cat_cols[i]:
            is_active = st.session_state.home_category == cat
            btn_label = f"**{label}**" if is_active else label
            if st.button(btn_label, key=f"cat_{cat}", use_container_width=True):
                st.session_state.home_category = cat
                st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    active_cat = st.session_state.home_category
    active_label = cat_labels[categories.index(active_cat)]
    st.markdown(
        f"<div class='section-heading'>{active_label} <span class='accent'>_</span></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading movies…"):
        home_cards, err = api_get_json(
            "/home", params={"category": active_cat, "limit": 24}
        )

    if err or not home_cards:
        st.error(f"Could not load home feed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=6, key_prefix="home_feed")


# =============================
# VIEW: DETAILS
# =============================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Back button
    st.markdown("<div class='back-btn-wrap'>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    with st.spinner("Loading movie details…"):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop (full-width, dimmed)
    if data.get("backdrop_url"):
        st.markdown(
            f"""
<div style="width:100%;max-height:340px;overflow:hidden;border-radius:20px;margin-bottom:1.5rem;
position:relative;">
  <img src="{data['backdrop_url']}" style="width:100%;object-fit:cover;border-radius:20px;
  filter:brightness(0.45) saturate(1.2);">
  <div style="position:absolute;inset:0;background:linear-gradient(to top,#08090d 0%,transparent 60%);border-radius:20px;"></div>
</div>
""",
            unsafe_allow_html=True,
        )

    # Poster + Details
    left, right = st.columns([1, 2.6], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div class='no-poster-box' style='height:400px'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)

        st.markdown(
            f"<div class='detail-title'>{data.get('title','')}</div>",
            unsafe_allow_html=True,
        )

        # Meta badges
        badges = []
        release = (data.get("release_date") or "")[:4]
        if release:
            badges.append(f"📅 {release}")
        for g in data.get("genres", [])[:4]:
            badges.append(g["name"])

        badge_html = "".join(
            [f"<span class='detail-badge'>{b}</span>" for b in badges]
        )
        st.markdown(
            f"<div class='detail-meta'>{badge_html}</div>", unsafe_allow_html=True
        )

        st.markdown(
            "<div style='height:0.25rem;width:48px;background:#dc3c1e;border-radius:2px;margin-bottom:1rem'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div class='detail-overview'>{data.get('overview') or 'No overview available.'}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── RECOMMENDATIONS ──
    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding recommendations…"):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            st.markdown(
                "<div class='section-heading'>🔎 Similar Movies <span class='accent'>_</span></div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=6,
                key_prefix="details_tfidf",
            )

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='section-heading'>🎭 More Like This <span class='accent'>_</span></div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=6,
                key_prefix="details_genre",
            )
        else:
            st.markdown(
                "<div class='section-heading'>🎭 You Might Also Like <span class='accent'>_</span></div>",
                unsafe_allow_html=True,
            )
            with st.spinner("Loading…"):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=6, key_prefix="details_genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available for recommendations.")