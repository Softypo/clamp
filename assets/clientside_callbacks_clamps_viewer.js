window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clamps_viewer: {
        tab_content: function (active_tab, cd_table_rowid) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);
            let on = { 'display': 'block', 'height': '100%' };
            let off = { 'display': 'none', 'height': '100%' };
            if (trigger == "cd_table" && Object.keys(cd_table_rowid).length > 0) return [off, false, on, true, 'tubeview']
            else if (active_tab == 'overview') return [on, true, off, false, 'overview']
            else return [off, false, on, true, 'tubeview']
        },
        cstore_switcher: function (themeToggle, unitsToggle, ctbl, cover, cpolar, themes) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);
            // ctbl_new = JSON.parse(JSON.stringify(ctbl));
            // cover_fig = JSON.parse(JSON.stringify(cover));
            // cpolar_fig = JSON.parse(JSON.stringify(cpolar));
            let ctbl_new = structuredClone(ctbl);
            let cover_fig = structuredClone(cover);
            let cpolar_fig = structuredClone(cpolar);
            // let ctbl_new = [...ctbl];
            // let cover_fig = { ...cover };
            // let cpolar_fig = { ...cpolar };
            // let cview_fig = structuredClone(cview);

            // console.log('pre u', cpolar_fig);

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
                // cview_fig.layout.template = template;
                // cview_fig.layout.modebar = modebar;
                //return [ctbl_new, cover_fig, cpolar_fig];
            };

            // if (trigger == "unitsToggle") {
            if (unitsToggle) {
                if (cover_fig.layout.yaxis.title.text == 'Depth (ft)') return [ctbl_new, cover_fig, cpolar_fig];
                cover_fig.data.forEach((trace, index) => {
                    cover_fig.data[index].y = trace.y.map(y => y * 3.28084);
                    cpolar_fig.data[index].r = cpolar_fig.data[index].r.map(y => y * 3.28084);
                    cpolar_fig.data[index].customdata = cpolar_fig.data[index].customdata.map(c => [c[0], +(c[1] * 3.28084).toFixed(0), c[2]]);
                    cpolar_fig.data[index].hovertemplate = '%{customdata[1]} ft<br>%{customdata[2]} deg (TOH)';
                });
                cover_fig.layout.yaxis.title.text = 'Depth (ft)';
                cover_fig.layout.yaxis.ticksuffix = ' ft';
                // delete cover_fig.layout.yaxis.range;
                cpolar_fig.layout.polar.radialaxis.range = [Math.max(...cpolar_fig.data[3].r) + 300, Math.min(...cpolar_fig.data[3].r) - 300];
                // cpolar_fig.layout['uirevision'] = ' ft';
                ctbl_new = ctbl_new.map(dic => Object.assign(dic, { 'depth': +(dic.depth * 3.28084).toFixed(3) }));
            } else {
                if (cover_fig.layout.yaxis.title.text == 'Depth (m)') return [ctbl_new, cover_fig, cpolar_fig];
                cover_fig.data.forEach((trace, index) => {
                    cover_fig.data[index].y = trace.y.map(y => y * 0.3048);
                    cpolar_fig.data[index].r = cpolar_fig.data[index].r.map(y => y * 0.3048);
                    cpolar_fig.data[index].customdata = cpolar_fig.data[index].customdata.map(c => [c[0], +(c[1] * 0.3048).toFixed(0), c[2]]);
                    cpolar_fig.data[index].hovertemplate = '%{customdata[1]} m<br>%{customdata[2]} deg (TOH)';
                });
                cover_fig.layout.yaxis.title.text = 'Depth (m)';
                cover_fig.layout.yaxis.ticksuffix = ' m';
                // delete cover_fig.layout.yaxis.range;
                cpolar_fig.layout.polar.radialaxis.range = [Math.max(...cpolar_fig.data[3].r) + 100, Math.min(...cpolar_fig.data[3].r) - 100];
                // cpolar_fig.layout['uirevision'] = ' m';
                ctbl_new = ctbl_new.map(dic => Object.assign(dic, { 'depth': +(dic.depth * 0.3048).toFixed(3) }));
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
            // };

            // cover_fig.layout.autosize = true;
            // delete cover_fig.layout.yaxis.autorange
            // cover_fig.layout.yaxis.autorange = true;
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

            if (trigger == "cd_overview" && Object.keys(relayoutData).length == 4) {
                if (relayoutData['xaxis.range[1]'] == relayoutData['xaxis.range[0]'] && relayoutData['yaxis.range[1]'] == relayoutData['yaxis.range[0]']) {
                    new_fig.layout.xaxis = { ...store_fig.layout.xaxis };
                    new_fig.layout.yaxis = { ...store_fig.layout.yaxis };
                };
                return new_fig;
            };

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
            if (trigger == "dropdown_cd" || fig === undefined) new_fig.layout.transition = { "duration": 500, "easing": "cubic-in-out" };

            return new_fig;
        },
        clampspolar_listener: function (clamps_types, relayoutData, store_fig, fig, unitsToggle) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);

            let new_fig;
            if (fig === undefined || trigger == "cpolar") {
                new_fig = structuredClone(store_fig);
            } else {
                new_fig = { ...fig };
            };

            if (trigger == "cd_overview" && Object.keys(relayoutData).length > 1) {
                //console.log(relayoutData);
                if (relayoutData['yaxis.range[0]'] != undefined && relayoutData['yaxis.range[0]'] != relayoutData['yaxis.range[1]']) {
                    new_fig.layout.polar.radialaxis.range = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']];
                } else if (relayoutData['yaxis.range[0]'] != undefined && relayoutData['yaxis.range[0]'] == relayoutData['yaxis.range[1]']) new_fig.layout.polar.radialaxis.range = [...store_fig.layout.polar.radialaxis.range];
                else if (relayoutData['xaxis.range[0]'] == undefined) new_fig.layout.polar.radialaxis.range = [...store_fig.layout.polar.radialaxis.range];
                // return new_fig;
            };

            let r = [];
            let theta = [];
            let c = [];
            let n = 0;
            let sum = 0;
            let stats = [];
            store_fig.data.forEach((trace, index) => {
                if (trace.name == "Fiber Wire") {
                    trace.customdata.forEach((type, indext) => {
                        if (clamps_types.includes(type[0])) {
                            r = r.concat(store_fig.data[index]['r'][indext]);
                            theta = theta.concat(store_fig.data[index]['theta'][indext]);
                            c = c.concat([type]);
                            if (r.at(-1) < new_fig.layout.polar.radialaxis.range[0] && r.at(-1) > new_fig.layout.polar.radialaxis.range[1]) {
                                n++;
                                sum = sum + theta.at(-1);
                                stats = stats.concat(theta.at(-1));
                            }
                        }
                    });
                    new_fig.data[index]['r'] = r;
                    new_fig.data[index]['theta'] = theta;
                    new_fig.data[index]['customdata'] = c;
                };
            });

            let units = unitsToggle ? "ft" : "m";
            let interval = `${new_fig.layout.polar.radialaxis.range[1].toFixed(2)} - ${new_fig.layout.polar.radialaxis.range[0].toFixed(2)} ${units}`;
            let mean
            let std
            if (Object.keys(stats).length > 0) {
                interval = `${new_fig.layout.polar.radialaxis.range[1].toFixed(2)} - ${new_fig.layout.polar.radialaxis.range[0].toFixed(2)} ${units}`;
                mean = sum > 0 ? `${(sum / n).toFixed(0)}°` : `${(360 + (sum / n)).toFixed(0)}°`;
                // let median = sum > 0 ? sum : 360 + sum;
                // median = median > 0 ? (median).toFixed(0) : (360 + median).toFixed(0);

                function dev(array) {
                    const n = array.length
                    const mean = array.reduce((a, b) => a + b) / n
                    return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
                }
                std = dev(stats).toFixed(2);
            };

            // console.log(interval);
            // console.log('mean', mean);
            // console.log(n);
            // console.log(sum);
            // console.log(new_fig);
            return [interval, mean, std, new_fig];
        },
        clampstable_listener: function (clamps_types, store_tbl, clickData, selected_rows) {
            const trigger = window.dash_clientside.callback_context.triggered.map(t => t.prop_id.split(".")[0]);
            let new_tbl = [];
            let new_cols = [];
            // if (new_tbl === undefined || trigger == "ctbl") {
            //     new_tbl = structuredClone(store_tbl);

            index = 0;
            store_tbl.forEach(row => {
                if (clamps_types.includes(row.type)) {
                    new_tbl[index] = { ...row };
                    index++;
                };
            });
            Object.keys(store_tbl[0]).forEach(key => {
                if (["id", "type"].includes(key) == false) new_cols = new_cols.concat({ "name": key, "id": key });
            });

            // console.log(clickData);
            // console.log(selected_rows);
            // console.log('tbl store', store_tbl);
            // console.log('tbl new', new_cols);
            if (trigger == "ctbl") return [new_tbl, new_cols, selected_rows];
            else return [new_tbl, new_cols, []];
        },
        clampstable_rowselect: function (rows) {
            let selected_rows = [];
            if (rows == undefined) return window.dash_clientside.no_update;
            rows.forEach(row => {
                selected_rows = selected_rows.concat({ "if": { "filter_query": `{id} = ${row}` }, "backgroundColor": '#e95420' });
            });
            // console.log('post', selected_rows);
            return selected_rows;
        },
        clampstable_tocsv: function (_, data) {
            if (data == undefined) return window.dash_clientside.no_update;
            const dictionaryKeys = Object.keys(data[0]).filter(key => key != "id")
            return [dictionaryKeys.join(','), ...data.map(dict => (dictionaryKeys.map(key => dict[key]).join(',')))].join("\n");
        },
    }
});