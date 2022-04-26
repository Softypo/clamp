window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            stylesheet.href = themeLink;
        },
        clampsoverview_listener: function (clamps_types, themeToggle, fig, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            console.log(window.dash_clientside);

            if (trigger == '' || trigger == undefined) {
                console.log("trigger is undefined");
                return dash_clientside.no_update;
            }
            else if (fig === undefined) {
                console.log("fig is undefined");
                return dash_clientside.no_update;
            }

            const new_fig = { ...fig };



            console.log(trigger);
            console.log(themeToggle);

            if (trigger == "themeToggle") {
                if (themeToggle) {
                    console.log("themeToggle_light");
                    //new_fig['layout']['template'] = _light
                    new_fig['layout']['modebar'] = {
                        'orientation': 'v',
                        'bgcolor': 'salmon',
                        'color': 'white',
                        'activecolor': '#9ED3CD'
                    };
                    //console.log(new_fig.layout.template)
                    //console.log(fig.layout.modebar)
                } else {
                    console.log("themeToggle_dark");
                    //new_fig['layout']['template'] = _light
                    new_fig['layout']['modebar'] = {
                        'orientation': 'v',
                        'bgcolor': 'rgb(39, 43, 48)',
                        'color': 'white',
                        'activecolor': 'grey'
                    };
                    //console.log(new_fig.layout.template)
                    //console.log(fig.layout.modebar)
                }
                // } else if (trigger === "dropdown_cd") {
                //     //console.log(nClicks);
                //     fig.data.forEach(trace => {
                //         if (trace.name in clamps_types) {
                //             trace.visibility = 'legendonly';
                //         } else {
                //             trace.visibility = True;
                //         }
                //     });
                // } else if (trigger === "relayoutData" && relayoutData !== undefined) {
                //     if (length(relayoutData) > 1) {
                //         if ('xaxis.range[1]' in relayoutData && 'yaxis.range[1]' in relayoutData) {
                //             if (relayoutData['xaxis.range[1]'] !== relayoutData['xaxis.range[0]'] && relayoutData['yaxis.range[1]'] !== relayoutData['yaxis.range[0]']) {
                //                 fig.layout.yaxis.autorange = "reversed";
                //             }
                //         }
                //     }
                // }
                // end of main function
            }
            console.log(new_fig);
            return new_fig;
        }
    }
});