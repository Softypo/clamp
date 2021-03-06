window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dv_dashboard: {
        toggle_navbar_collapse: function (n_clicks, is_open) {
            if (n_clicks) return ~is_open
            else return is_open
        },
        close_sidebar: function (sidebar_toggler, n_clicks, is_open_sidebar, navbar_toggler_n_clicks) {
            if (window.innerWidth < 992) navbar_toggler_n_clicks++;
            if (n_clicks) return [[1], false, navbar_toggler_n_clicks, 0];
            else if (sidebar_toggler == false) return [sidebar_toggler, true, 0, n_clicks];
            else if (sidebar_toggler) return [sidebar_toggler, false, 0, n_clicks];
            else return [sidebar_toggler, is_open_sidebar, 0, n_clicks];
        },
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            setTimeout(function () { stylesheet.href = themeLink; }, 100);
            if (themeToggle) return { "colorScheme": "light" };
            else return { "colorScheme": "dark" };
        },
        // first_load_delay: function (void) {
        //     let out;
        //     setTimeout(function () { out = true; }, 100);
        //     return true;
        // },
    }
});