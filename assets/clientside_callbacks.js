window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            //stylesheet.href = themeLink;
            setTimeout(function () { stylesheet.href = themeLink; }, 100);
        },
        cstore_switcher: function (themeToggle, unitsToggle, ctbl, cover, cpolar, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);
            // ctbl_new = JSON.parse(JSON.stringify(ctbl));
            // cover_fig = JSON.parse(JSON.stringify(cover));
            // cpolar_fig = JSON.parse(JSON.stringify(cpolar));
            let ctbl_new = [...ctbl];
            let cover_fig = { ...cover };
            let cpolar_fig = { ...cpolar };
            console.log('pre u', ctbl);

            if (trigger == "themeToggle" || cover_fig.layout.template.theme === undefined) {
                let template = {};
                let modebar = {};
                if (themeToggle && (cover_fig.layout.template.theme == '_dark' || cover_fig.layout.template.theme === undefined)) {
                    const request = new XMLHttpRequest();
                    request.open('GET', themes['_light']['json'], false); // true creates a promise, so it wont work
                    request.send();
                    template = JSON.parse(request.response);
                    template['theme'] = '_light';
                    modebar = {
                        'orientation': 'v',
                        'bgcolor': 'salmon',
                        'color': 'white',
                        'activecolor': '#9ED3CD'
                    };
                } else if (cover_fig.layout.template.theme == '_light' || cover_fig.layout.template.theme === undefined) {
                    const request = new XMLHttpRequest();
                    request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
                    request.send();
                    template = JSON.parse(request.response);
                    template['theme'] = '_dark';
                    modebar = {
                        'orientation': 'v',
                        'bgcolor': 'rgb(39, 43, 48)',
                        'color': 'white',
                        'activecolor': 'grey'
                    };
                } else {
                    template = cover_fig.layout.template;
                    modebar = cover_fig.layout.modebar;
                };
                cover_fig.layout.template = template;
                cover_fig.layout.modebar = modebar;
                cpolar_fig.layout.template = template;
                cpolar_fig.layout.modebar = modebar;
            };

            if (trigger == "unitsToggle") {
                if (unitsToggle) {
                    if (cover_fig.layout.yaxis.title.text == 'Depth (ft)') return [ctbl, cover_fig, cpolar_fig];
                    cover_fig.data.forEach((trace, index) => {
                        cover_fig.data[index].y = trace.y.map(y => y * 3.28084);
                        cpolar_fig.data[index].r = cpolar_fig.data[index].r.map(y => y * 3.28084);
                        cpolar_fig.data[index].customdata = cpolar_fig.data[index].customdata.map(c => [c[0], c[1] * 3.28084, c[2]]);
                        cpolar_fig.data[index].hovertemplate = '%{customdata[1]} ft<br>%{customdata[2]} deg (TOH)';
                    });
                    cover_fig.layout.yaxis.title.text = 'Depth (ft)';
                    cover_fig.layout.yaxis.ticksuffix = ' ft';
                    // delete cover_fig.layout.yaxis.range;
                    cpolar_fig.layout.polar.radialaxis.range = [Math.max(...cpolar_fig.data[3].r) + 300, Math.min(...cpolar_fig.data[3].r) - 300];
                    ctbl_new = ctbl_new.map(dic => Object.assign(dic, { 'depth': dic.depth * 3.28084 }));
                } else {
                    if (cover_fig.layout.yaxis.title.text == 'Depth (m)') return [ctbl, cover_fig, cpolar_fig];
                    cover_fig.data.forEach((trace, index) => {
                        cover_fig.data[index].y = trace.y.map(y => y * 0.3048);
                        cpolar_fig.data[index].r = cpolar_fig.data[index].r.map(y => y * 0.3048);
                        cpolar_fig.data[index].customdata = cpolar_fig.data[index].customdata.map(c => [c[0], c[1] * 0.3048, c[2]]);
                        cpolar_fig.data[index].hovertemplate = '%{customdata[1]} m<br>%{customdata[2]} deg (TOH)';
                    });
                    cover_fig.layout.yaxis.title.text = 'Depth (m)';
                    cover_fig.layout.yaxis.ticksuffix = ' m';
                    // delete cover_fig.layout.yaxis.range;
                    cpolar_fig.layout.polar.radialaxis.range = [Math.max(...cpolar_fig.data[3].r) + 100, Math.min(...cpolar_fig.data[3].r) - 100];
                    ctbl_new = ctbl_new.map(dic => Object.assign(dic, { 'depth': dic.depth * 3.28084 }));
                };
                let nogozone_go = [];
                let nogozone_back = [];
                cover_fig.data.forEach((trace, index) => {
                    if (trace.name == "Fiber Wire") {
                        trace.customdata.forEach((type, indext) => {
                            nogozone_go = nogozone_go.concat(`L${cover_fig.data[index]['x'][indext] - 20},${cover_fig.data[index]['y'][indext]}`);
                            nogozone_back = nogozone_back.concat(`L${cover_fig.data[index]['x'][indext] + 20},${cover_fig.data[index]['y'][indext]}`);
                        });
                        if (nogozone_go[0] != undefined) {
                            nogozone_go[0] = nogozone_go[0].replace('L', 'M ');
                            nogozone_back[0] = nogozone_back[0] + ' Z';
                        };
                        cover_fig.layout.shapes[0]['path'] = nogozone_go + nogozone_back.reverse();
                    };
                });
            };

            // cover_fig.layout.autosize = true;
            // delete cover_fig.layout.yaxis.autorange
            // cover_fig.layout.yaxis.autorange = true;
            console.log('post u', ctbl_new);
            return [ctbl_new, cover_fig, cpolar_fig];
        },
        clampsoverview_listener: function (clamps_types, relayoutData, store_fig, fig) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            let new_fig;
            if (fig === undefined || trigger == "cover") {
                new_fig = structuredClone(store_fig);
            } else {
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
                // delete new_fig.layout.transition;
                return new_fig;
            };

            // if (themeToggle) {
            //     const request = new XMLHttpRequest();
            //     request.open('GET', themes['_light']['json'], false); // true creates a promise, so it wont work
            //     request.send();
            //     new_fig['layout']['template'] = JSON.parse(request.response);
            //     new_fig['layout']['modebar'] = {
            //         'orientation': 'v',
            //         'bgcolor': 'salmon',
            //         'color': 'white',
            //         'activecolor': '#9ED3CD'
            //     };
            //     //console.log(new_fig.layout.template)
            //     //console.log(fig.layout.modebar)
            // } else {
            //     const request = new XMLHttpRequest();
            //     request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
            //     request.send();
            //     new_fig['layout']['template'] = JSON.parse(request.response);
            //     new_fig['layout']['modebar'] = {
            //         'orientation': 'v',
            //         'bgcolor': 'rgb(39, 43, 48)',
            //         'color': 'white',
            //         'activecolor': 'grey'
            //     };
            // };
            // if (trigger == "themeToggle") { delete new_fig.layout.transition; return new_fig; };

            if (trigger == "dropdown_cd" || fig === undefined) {
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
                new_fig.layout.transition = { "duration": 500, "easing": "cubic-in-out" };
            };


            // end of main function
            // console.log(new_fig);
            // console.log(store);
            return new_fig;
        },
        clampspolar_listener: function (clamps_types, store_fig, fig) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            let new_fig;
            if (fig === undefined || trigger == "cpolar") {
                new_fig = structuredClone(store_fig);
            } else {
                new_fig = { ...fig };
            };

            // console.log(trigger);
            // console.log(themeToggle);

            // if (themeToggle) {
            //     const request = new XMLHttpRequest();
            //     request.open('GET', themes['_light']['json'], false); // true creates a promise, so it wont work
            //     request.send();
            //     new_fig['layout']['template'] = JSON.parse(request.response);
            //     new_fig['layout']['modebar'] = {
            //         'orientation': 'v',
            //         'bgcolor': 'salmon',
            //         'color': 'white',
            //         'activecolor': '#9ED3CD'
            //     };
            //     //console.log(new_fig.layout.template)
            //     //console.log(fig.layout.modebar)
            // } else {
            //     const request = new XMLHttpRequest();
            //     request.open('GET', themes['_dark']['json'], false); // true creates a promise, so it wont work
            //     request.send();
            //     new_fig['layout']['template'] = JSON.parse(request.response);
            //     new_fig['layout']['modebar'] = {
            //         'orientation': 'v',
            //         'bgcolor': 'rgb(39, 43, 48)',
            //         'color': 'white',
            //         'activecolor': 'grey'
            //     };
            // };

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