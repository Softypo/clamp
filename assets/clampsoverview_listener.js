window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        clampsoverview_listener: function (clamps_types, themeToggle, relayoutData, fig, themes) {
            // storeURLs is an array that holds the image URLs
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[1]);
            console.log(fig);

            // if (fig === undefined) {
            //     return dash_clientside.no_update;
            // }

            if (trigger === "themeToggle") {
                if (themeToggle) {
                    fig.layout.template = themes._light.fig
                    fig.layout.modebar = {
                        'orientation': 'v',
                        'bgcolor': 'salmon',
                        'color': 'white',
                        'activecolor': '#9ED3CD'
                    }
                } else {
                    fig.layout.template = themes._dark.fig
                    fig.layout.modebar = {
                        'orientation': 'v',
                        'bgcolor': 'rgb(39, 43, 48)',
                        'color': 'white',
                        'activecolor': 'grey'
                    }
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
            return fig;
        }
    }
});