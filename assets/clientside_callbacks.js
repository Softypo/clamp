window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            //stylesheet.href = themeLink;
            setTimeout(function () { stylesheet.href = themeLink; }, 500);
        },
        units_switcher: function (unitsToggle, store) {
            new_fig = JSON.parse(JSON.stringify(store));
            console.log('pre u', new_fig);
            if (unitsToggle) {
                if (new_fig.layout.yaxis.title.text == 'Depth (ft)') return new_fig;
                new_fig.data.forEach((trace, index) => {
                    //ft = trace.y * 3.28084;
                    console.log(index);
                    new_fig.data[index].y = trace.y.map(y => y * 3.28084);
                });
                new_fig.layout.yaxis.title.text = 'Depth (ft)';
                new_fig.layout.yaxis.ticksuffix = ' ft';
                // delete new_fig.layout.yaxis.range;
            } else {
                if (new_fig.layout.yaxis.title.text == 'Depth (m)') return new_fig;
                new_fig.data.forEach((trace, index) => {
                    //ft = trace.y * 3.28084;
                    console.log(index);
                    new_fig.data[index].y = trace.y.map(y => y * 0.3048);
                });
                new_fig.layout.yaxis.title.text = 'Depth (m)';
                new_fig.layout.yaxis.ticksuffix = ' m';
                // delete new_fig.layout.yaxis.range;
            };
            new_fig.layout.autosize = true;
            // delete new_fig.layout.yaxis.autorange
            // new_fig.layout.yaxis.range = [Math.max(...new_fig.data[3].y), Math.min(...new_fig.data[3].y)];
            console.log('port u', new_fig);
            return new_fig;
        },
        clampsoverview_listener: function (clamps_types, themeToggle, relayoutData, store, fig, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            new_fig = {};
            if (fig === undefined || trigger == "cover") {
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = JSON.parse(JSON.stringify(store));
            } else {
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = { ...fig };
            };

            // if (trigger == "unitsToggle") {
            //     if (unitsToggle) {
            //         new_fig.data.forEach((trace, index) => {
            //             ft = trace.y * 3.28084;
            //             new_fig.data[index].y = new_fig.data[index].y.map(y => y * 3.28084);
            //         });
            //         delete new_fig.layout.yaxis.range;
            //         // new_fig.layout.yaxis.range = new_fig.layout.yaxis.range.map(y => y * 3.28084);
            //     };
            // };

            // console.log(trigger);
            // console.log(themeToggle);

            //console.log("_fig", new_fig);

            if (trigger == "cd_overview" && Object.keys(relayoutData).length == 4) {
                // console.log(Object.keys(relayoutData).length);
                if (relayoutData['xaxis.range[1]'] == relayoutData['xaxis.range[0]'] && relayoutData['yaxis.range[1]'] == relayoutData['yaxis.range[0]']) {
                    new_fig.layout.xaxis = { ...store_fig.layout.xaxis };
                    new_fig.layout.yaxis = { ...store_fig.layout.yaxis };
                    // new_fig = { ...store_fig };
                }
                return new_fig;
            };

            if (themeToggle) {
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
                const request = new XMLHttpRequest();
                request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
                request.send();
                new_fig['layout']['template'] = JSON.parse(request.response);
                new_fig['layout']['modebar'] = {
                    'orientation': 'v',
                    'bgcolor': 'rgb(39, 43, 48)',
                    'color': 'white',
                    'activecolor': 'grey'
                };
            };
            if (trigger == "themeToggle") { console.log('r', new_fig); return new_fig; };


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
                            nogozone_go = nogozone_go.concat(`L${store_fig.data[index]['x'][indext] - 20},${store_fig.data[index]['y'][indext]}`);
                            nogozone_back = nogozone_back.concat(`L${store_fig.data[index]['x'][indext] + 20},${store_fig.data[index]['y'][indext]}`);
                        }
                    });
                    if (nogozone_go[0] != undefined) {
                        nogozone_go[0] = nogozone_go[0].replace('L', 'M ');
                        nogozone_back[0] = nogozone_back[0] + ' Z';
                    };
                    new_fig.data[index]['y'] = y;
                    new_fig.data[index]['x'] = x;
                    new_fig.data[index]['customdata'] = c;
                    new_fig.layout.shapes[0]['path'] = nogozone_go + nogozone_back.reverse();
                };
            });


            // end of main function
            // console.log(new_fig);
            // console.log(store);
            return new_fig;
        },
        clampspolar_listener: function (clamps_types, themeToggle, fig, store, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            new_fig = {};
            if (fig === undefined) {
                // console.log("fig is undefined");
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = JSON.parse(JSON.stringify(store));
            } else {
                store_fig = JSON.parse(JSON.stringify(store));
                new_fig = { ...fig };
            };

            // console.log(trigger);
            // console.log(themeToggle);

            if (themeToggle) {
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
                const request = new XMLHttpRequest();
                request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
                request.send();
                new_fig['layout']['template'] = JSON.parse(request.response);
                new_fig['layout']['modebar'] = {
                    'orientation': 'v',
                    'bgcolor': 'rgb(39, 43, 48)',
                    'color': 'white',
                    'activecolor': 'grey'
                };
            };
            let r = [];
            let theta = [];
            let c = [];
            store_fig.data.forEach((trace, index) => {
                if (trace.name == "Fiber Wire") {
                    trace.customdata.forEach((type, indext) => {
                        if (clamps_types.includes(type[0])) {
                            r = r.concat(store_fig.data[index]['r'][indext]);
                            theta = theta.concat(store_fig.data[index]['theta'][indext]);
                            c = c.concat([type]);
                        }
                    });
                    new_fig.data[index]['r'] = r;
                    new_fig.data[index]['theta'] = theta;
                    new_fig.data[index]['customdata'] = c;
                };
            });
            // end of main function
            // console.log(new_fig);
            // console.log(store);
            return new_fig;
        },
    }
});