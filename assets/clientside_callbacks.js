window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            //stylesheet.href = themeLink;
            setTimeout(function () { stylesheet.href = themeLink; }, 500);
        },
        clampsoverview_listener: function (clamps_types, themeToggle, relayoutData, fig, store, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            new_fig = {};
            if (fig === undefined) {
                console.log("fig is undefined");
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = JSON.parse(JSON.stringify(store));
            } else {
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = { ...fig };

            };
            // if (trigger == '' || trigger == undefined) {
            //     console.log("trigger is undefined");
            //     return dash_clientside.no_update;
            // }
            // else if (store === undefined) {
            //     console.log("store fig is undefined");
            //     return dash_clientside.no_update;
            // }
            // else if (fig === undefined) {
            //     console.log("fig is undefined");
            //     new_fig = { ...store };
            // }
            // if (trigger == 'cd_overview') {
            //     console.log("cd no update");
            //     return dash_clientside.no_update;
            // }

            console.log(trigger);
            console.log(themeToggle);

            // if (trigger == "themeToggle") {
            if (themeToggle) {
                console.log("themeToggle_light");
                // new_fig['layout']['template'] = await fetch(themes['_light']['json'])
                // .then(url => url.json())
                // .then(output => { new_fig['layout']['template'] = output; console.log(output) })
                // new_fig['layout']['template'] = _light
                const request = new XMLHttpRequest();
                request.open('GET', themes['_light']['json'], false); // true creates a promise, so it wont work
                request.send();
                new_fig['layout']['template'] = JSON.parse(request.response);
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
                console.log(themes['_dark']['json']);
                // url = fetch(themes['_dark']['json'])
                // console.log(url);
                // new_fig['layout']['template'] = url.json();
                // fetch(themes['_dark']['json']).then(url => url.json()).then(data => new_fig['layout']['template'] = data);
                // $.getJSON(themes['_dark']['json'], function(data) {new_fig['layout']['template'] = data});
                // new_fig['layout']['template'] = fetch(themes['_dark']['json'])
                //     .then(url => { console.log(url); url.response.json() })
                //     .then(output => { new_fig['layout']['template'] = output; console.log(output) })
                const request = new XMLHttpRequest();
                request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
                request.send();
                new_fig['layout']['template'] = JSON.parse(request.response);
                // new_fig['layout']['template'] = template
                // new_fig['layout']['template']['layout'] = _dark
                new_fig['layout']['modebar'] = {
                    'orientation': 'v',
                    'bgcolor': 'rgb(39, 43, 48)',
                    'color': 'white',
                    'activecolor': 'grey'
                };
            }
            // }
            //console.log(new_fig.layout.template)
            //console.log(fig.layout.modebar)
            //}
            // if (trigger == "dropdown_cd") {
            //console.log(nClicks);
            let y = [];
            let x = [];
            let c = [];
            let nogozone_go = [];
            let nogozone_back = [];
            store_fig.data.forEach((trace, index) => {
                if (trace.name == "Fiber Wire") {
                    trace.customdata.forEach((type, indext) => {
                        if (clamps_types.includes(type[0])) {
                            y = y.concat(store_fig.data[index]['y'][indext]);
                            x = x.concat(store_fig.data[index]['x'][indext]);
                            c = c.concat([type]);
                            nogozone_go = nogozone_go.concat(`L${store_fig.data[index]['x'][indext] - 10},${store_fig.data[index]['y'][indext]}`);
                            nogozone_back = nogozone_back.concat(`L${store_fig.data[index]['x'][indext] + 10},${store_fig.data[index]['y'][indext]}`);
                        }
                    });
                    if (nogozone_go[0] != undefined) {
                        nogozone_go[0] = nogozone_go[0].replace('L', 'M ');
                        nogozone_back[0] = nogozone_back[0] + ' Z';
                    };
                    //console.log(c);
                    //y = y.sort((a, b) => a - b);
                    new_fig.data[index]['y'] = y;
                    new_fig.data[index]['x'] = x //.sort((a, b) => y.indexOf(a) - y.indexOf(b));
                    new_fig.data[index]['customdata'] = c //.sort((a, b) => y.indexOf(a) - y.indexOf(b));
                    new_fig.layout.shapes[0]['path'] = nogozone_go + nogozone_back.reverse();
                    //trace.visibility = false;
                    //console.log(clamps_types);
                    //console.log(y.length);
                    //console.log(new_fig.data[index]['y'].length);
                }
            });
            // };
            if (trigger === "relayoutData" && relayoutData !== undefined) {
                if (length(relayoutData) > 1) {
                    if ('xaxis.range[1]' in relayoutData && 'yaxis.range[1]' in relayoutData) {
                        if (relayoutData['xaxis.range[1]'] !== relayoutData['xaxis.range[0]'] && relayoutData['yaxis.range[1]'] !== relayoutData['yaxis.range[0]']) {
                            fig.layout.yaxis.autorange = "reversed";
                        }
                    }
                }
            };
            // end of main function
            console.log(new_fig);
            console.log(store);
            return new_fig;
        }
    }
});