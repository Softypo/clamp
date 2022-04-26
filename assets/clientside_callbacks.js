window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        theme_switcher: function (themeToggle, themes) {
            const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]');
            var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
            stylesheet.href = themeLink;
        },
        clampsoverview_listener: function (clamps_types, themeToggle, relayoutData, fig, themes) {
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

            const _dark = {
                "annotationdefaults": {
                    "arrowcolor": "#f2f5fa",
                    "arrowhead": 0,
                    "arrowwidth": 1
                },
                "autotypenumbers": "strict",
                "coloraxis": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "ticks": ""
                    }
                },
                "colorscale": {
                    "diverging": [
                        [
                            0,
                            "#8e0152"
                        ],
                        [
                            0.1,
                            "#c51b7d"
                        ],
                        [
                            0.2,
                            "#de77ae"
                        ],
                        [
                            0.3,
                            "#f1b6da"
                        ],
                        [
                            0.4,
                            "#fde0ef"
                        ],
                        [
                            0.5,
                            "#f7f7f7"
                        ],
                        [
                            0.6,
                            "#e6f5d0"
                        ],
                        [
                            0.7,
                            "#b8e186"
                        ],
                        [
                            0.8,
                            "#7fbc41"
                        ],
                        [
                            0.9,
                            "#4d9221"
                        ],
                        [
                            1,
                            "#276419"
                        ]
                    ],
                    "sequential": [
                        [
                            0,
                            "#3a3f44"
                        ],
                        [
                            0.1,
                            "#52484b"
                        ],
                        [
                            0.2,
                            "#6a5053"
                        ],
                        [
                            0.30000000000000004,
                            "#82595a"
                        ],
                        [
                            0.4,
                            "#9a6262"
                        ],
                        [
                            0.5,
                            "#b26b69"
                        ],
                        [
                            0.6000000000000001,
                            "#c97370"
                        ],
                        [
                            0.7000000000000001,
                            "#e17c78"
                        ],
                        [
                            0.8,
                            "#f9857f"
                        ],
                        [
                            0.9,
                            "#ff8d86"
                        ],
                        [
                            1,
                            "#ff968e"
                        ]
                    ],
                    "sequentialminus": [
                        [
                            0,
                            "#0d0887"
                        ],
                        [
                            0.1111111111111111,
                            "#46039f"
                        ],
                        [
                            0.2222222222222222,
                            "#7201a8"
                        ],
                        [
                            0.3333333333333333,
                            "#9c179e"
                        ],
                        [
                            0.4444444444444444,
                            "#bd3786"
                        ],
                        [
                            0.5555555555555556,
                            "#d8576b"
                        ],
                        [
                            0.6666666666666666,
                            "#ed7953"
                        ],
                        [
                            0.7777777777777778,
                            "#fb9f3a"
                        ],
                        [
                            0.8888888888888888,
                            "#fdca26"
                        ],
                        [
                            1,
                            "#f0f921"
                        ]
                    ]
                },
                "colorway": [
                    "#5d6167",
                    "#bd3539",
                    "#06a843",
                    "#f19502",
                    "#7dd3f2"
                ],
                "font": {
                    "color": "#aaa",
                    "family": "system-ui,-apple-system,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,\"Noto Sans\",\"Liberation Sans\",sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\",\"Noto Color Emoji\""
                },
                "geo": {
                    "bgcolor": "#272b30",
                    "lakecolor": "#272b30",
                    "landcolor": "#272b30",
                    "showlakes": true,
                    "showland": true,
                    "subunitcolor": "#506784"
                },
                "hoverlabel": {
                    "align": "left"
                },
                "hovermode": "closest",
                "mapbox": {
                    "style": "dark"
                },
                "margin": {
                    "b": 0,
                    "l": 0,
                    "r": 0
                },
                "paper_bgcolor": "#32383e",
                "piecolorway": [
                    "#5d6167",
                    "#bd3539",
                    "#06a843",
                    "#f19502",
                    "#7dd3f2"
                ],
                "plot_bgcolor": "#272b30",
                "polar": {
                    "angularaxis": {
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "ticks": ""
                    },
                    "bgcolor": "rgb(17,17,17)",
                    "radialaxis": {
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "ticks": ""
                    }
                },
                "scene": {
                    "xaxis": {
                        "backgroundcolor": "rgb(17,17,17)",
                        "gridcolor": "#506784",
                        "gridwidth": 2,
                        "linecolor": "#506784",
                        "showbackground": true,
                        "ticks": "",
                        "zerolinecolor": "#C8D4E3"
                    },
                    "yaxis": {
                        "backgroundcolor": "rgb(17,17,17)",
                        "gridcolor": "#506784",
                        "gridwidth": 2,
                        "linecolor": "#506784",
                        "showbackground": true,
                        "ticks": "",
                        "zerolinecolor": "#C8D4E3"
                    },
                    "zaxis": {
                        "backgroundcolor": "rgb(17,17,17)",
                        "gridcolor": "#506784",
                        "gridwidth": 2,
                        "linecolor": "#506784",
                        "showbackground": true,
                        "ticks": "",
                        "zerolinecolor": "#C8D4E3"
                    }
                },
                "shapedefaults": {
                    "line": {
                        "color": "#f2f5fa"
                    }
                },
                "sliderdefaults": {
                    "bgcolor": "#C8D4E3",
                    "bordercolor": "rgb(17,17,17)",
                    "borderwidth": 1,
                    "tickwidth": 0
                },
                "ternary": {
                    "aaxis": {
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "ticks": ""
                    },
                    "baxis": {
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "ticks": ""
                    },
                    "bgcolor": "rgb(17,17,17)",
                    "caxis": {
                        "gridcolor": "#506784",
                        "linecolor": "#506784",
                        "ticks": ""
                    }
                },
                "title": {
                    "x": 0.05
                },
                "updatemenudefaults": {
                    "bgcolor": "#506784",
                    "borderwidth": 0
                },
                "xaxis": {
                    "automargin": true,
                    "gridcolor": "#31353a",
                    "gridwidth": 0.5,
                    "linecolor": "#506784",
                    "ticks": "",
                    "title": {
                        "standoff": 15
                    },
                    "zerolinecolor": "#31353a",
                    "zerolinewidth": 2
                },
                "yaxis": {
                    "automargin": true,
                    "gridcolor": "#31353a",
                    "gridwidth": 0.5,
                    "linecolor": "#506784",
                    "ticks": "",
                    "title": {
                        "standoff": 15
                    },
                    "zerolinecolor": "#31353a",
                    "zerolinewidth": 2
                }
            }

            const _light = {
                "data": {
                    "barpolar": [
                        {
                            "marker": {
                                "line": {
                                    "color": "white",
                                    "width": 0.5
                                },
                                "pattern": {
                                    "fillmode": "overlay",
                                    "size": 10,
                                    "solidity": 0.2
                                }
                            },
                            "type": "barpolar"
                        }
                    ],
                    "bar": [
                        {
                            "error_x": {
                                "color": "#2a3f5f"
                            },
                            "error_y": {
                                "color": "#2a3f5f"
                            },
                            "marker": {
                                "line": {
                                    "color": "white",
                                    "width": 0.5
                                },
                                "pattern": {
                                    "fillmode": "overlay",
                                    "size": 10,
                                    "solidity": 0.2
                                }
                            },
                            "type": "bar"
                        }
                    ],
                    "carpet": [
                        {
                            "aaxis": {
                                "endlinecolor": "#2a3f5f",
                                "gridcolor": "#C8D4E3",
                                "linecolor": "#C8D4E3",
                                "minorgridcolor": "#C8D4E3",
                                "startlinecolor": "#2a3f5f"
                            },
                            "baxis": {
                                "endlinecolor": "#2a3f5f",
                                "gridcolor": "#C8D4E3",
                                "linecolor": "#C8D4E3",
                                "minorgridcolor": "#C8D4E3",
                                "startlinecolor": "#2a3f5f"
                            },
                            "type": "carpet"
                        }
                    ],
                    "choropleth": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "type": "choropleth"
                        }
                    ],
                    "contourcarpet": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "type": "contourcarpet"
                        }
                    ],
                    "contour": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "contour"
                        }
                    ],
                    "heatmapgl": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "heatmapgl"
                        }
                    ],
                    "heatmap": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "heatmap"
                        }
                    ],
                    "histogram2dcontour": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "histogram2dcontour"
                        }
                    ],
                    "histogram2d": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "histogram2d"
                        }
                    ],
                    "histogram": [
                        {
                            "marker": {
                                "pattern": {
                                    "fillmode": "overlay",
                                    "size": 10,
                                    "solidity": 0.2
                                }
                            },
                            "type": "histogram"
                        }
                    ],
                    "mesh3d": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "type": "mesh3d"
                        }
                    ],
                    "parcoords": [
                        {
                            "line": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "parcoords"
                        }
                    ],
                    "pie": [
                        {
                            "automargin": true,
                            "type": "pie"
                        }
                    ],
                    "scatter3d": [
                        {
                            "line": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scatter3d"
                        }
                    ],
                    "scattercarpet": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scattercarpet"
                        }
                    ],
                    "scattergeo": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scattergeo"
                        }
                    ],
                    "scattergl": [
                        {
                            "marker": {
                                "line": {
                                    "color": "#fff"
                                }
                            },
                            "type": "scattergl"
                        }
                    ],
                    "scattermapbox": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scattermapbox"
                        }
                    ],
                    "scatterpolargl": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scatterpolargl"
                        }
                    ],
                    "scatterpolar": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scatterpolar"
                        }
                    ],
                    "scatter": [
                        {
                            "marker": {
                                "line": {
                                    "color": "#fff"
                                }
                            },
                            "type": "scatter"
                        }
                    ],
                    "scatterternary": [
                        {
                            "marker": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "type": "scatterternary"
                        }
                    ],
                    "surface": [
                        {
                            "colorbar": {
                                "outlinewidth": 0,
                                "ticks": ""
                            },
                            "colorscale": [
                                [
                                    0,
                                    "#0d0887"
                                ],
                                [
                                    0.1111111111111111,
                                    "#46039f"
                                ],
                                [
                                    0.2222222222222222,
                                    "#7201a8"
                                ],
                                [
                                    0.3333333333333333,
                                    "#9c179e"
                                ],
                                [
                                    0.4444444444444444,
                                    "#bd3786"
                                ],
                                [
                                    0.5555555555555556,
                                    "#d8576b"
                                ],
                                [
                                    0.6666666666666666,
                                    "#ed7953"
                                ],
                                [
                                    0.7777777777777778,
                                    "#fb9f3a"
                                ],
                                [
                                    0.8888888888888888,
                                    "#fdca26"
                                ],
                                [
                                    1,
                                    "#f0f921"
                                ]
                            ],
                            "type": "surface"
                        }
                    ],
                    "table": [
                        {
                            "cells": {
                                "fill": {
                                    "color": "#EBF0F8"
                                },
                                "line": {
                                    "color": "white"
                                }
                            },
                            "header": {
                                "fill": {
                                    "color": "#C8D4E3"
                                },
                                "line": {
                                    "color": "white"
                                }
                            },
                            "type": "table"
                        }
                    ]
                },
                "layout": {
                    "annotationdefaults": {
                        "arrowcolor": "#2a3f5f",
                        "arrowhead": 0,
                        "arrowwidth": 1
                    },
                    "autotypenumbers": "strict",
                    "coloraxis": {
                        "colorbar": {
                            "outlinewidth": 0,
                            "ticks": ""
                        }
                    },
                    "colorscale": {
                        "diverging": [
                            [
                                0,
                                "#8e0152"
                            ],
                            [
                                0.1,
                                "#c51b7d"
                            ],
                            [
                                0.2,
                                "#de77ae"
                            ],
                            [
                                0.3,
                                "#f1b6da"
                            ],
                            [
                                0.4,
                                "#fde0ef"
                            ],
                            [
                                0.5,
                                "#f7f7f7"
                            ],
                            [
                                0.6,
                                "#e6f5d0"
                            ],
                            [
                                0.7,
                                "#b8e186"
                            ],
                            [
                                0.8,
                                "#7fbc41"
                            ],
                            [
                                0.9,
                                "#4d9221"
                            ],
                            [
                                1,
                                "#276419"
                            ]
                        ],
                        "sequential": [
                            [
                                0,
                                "#2c3e50"
                            ],
                            [
                                0.1,
                                "#454553"
                            ],
                            [
                                0.2,
                                "#5d4c56"
                            ],
                            [
                                0.30000000000000004,
                                "#765359"
                            ],
                            [
                                0.4,
                                "#8f5a5c"
                            ],
                            [
                                0.5,
                                "#a7615f"
                            ],
                            [
                                0.6000000000000001,
                                "#c06861"
                            ],
                            [
                                0.7000000000000001,
                                "#d96f64"
                            ],
                            [
                                0.8,
                                "#f17667"
                            ],
                            [
                                0.9,
                                "#ff7d6a"
                            ],
                            [
                                1,
                                "#ff846d"
                            ]
                        ],
                        "sequentialminus": [
                            [
                                0,
                                "#0d0887"
                            ],
                            [
                                0.1111111111111111,
                                "#46039f"
                            ],
                            [
                                0.2222222222222222,
                                "#7201a8"
                            ],
                            [
                                0.3333333333333333,
                                "#9c179e"
                            ],
                            [
                                0.4444444444444444,
                                "#bd3786"
                            ],
                            [
                                0.5555555555555556,
                                "#d8576b"
                            ],
                            [
                                0.6666666666666666,
                                "#ed7953"
                            ],
                            [
                                0.7777777777777778,
                                "#fb9f3a"
                            ],
                            [
                                0.8888888888888888,
                                "#fdca26"
                            ],
                            [
                                1,
                                "#f0f921"
                            ]
                        ]
                    },
                    "colorway": [
                        "#526074",
                        "#b71e1d",
                        "#06a843",
                        "#ec9d0e",
                        "#78b8ff"
                    ],
                    "font": {
                        "color": "#212529",
                        "family": "Lato,-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\""
                    },
                    "geo": {
                        "bgcolor": "#fff",
                        "lakecolor": "#fff",
                        "landcolor": "#fff",
                        "showlakes": true,
                        "showland": true,
                        "subunitcolor": "#C8D4E3"
                    },
                    "hoverlabel": {
                        "align": "left"
                    },
                    "hovermode": "closest",
                    "mapbox": {
                        "style": "light"
                    },
                    "margin": {
                        "b": 0,
                        "l": 0,
                        "r": 0
                    },
                    "paper_bgcolor": "#ffffff",
                    "piecolorway": [
                        "#526074",
                        "#b71e1d",
                        "#06a843",
                        "#ec9d0e",
                        "#78b8ff"
                    ],
                    "plot_bgcolor": "#fff",
                    "polar": {
                        "angularaxis": {
                            "gridcolor": "#EBF0F8",
                            "linecolor": "#EBF0F8",
                            "ticks": ""
                        },
                        "bgcolor": "white",
                        "radialaxis": {
                            "gridcolor": "#EBF0F8",
                            "linecolor": "#EBF0F8",
                            "ticks": ""
                        }
                    },
                    "scene": {
                        "xaxis": {
                            "backgroundcolor": "white",
                            "gridcolor": "#DFE8F3",
                            "gridwidth": 2,
                            "linecolor": "#EBF0F8",
                            "showbackground": true,
                            "ticks": "",
                            "zerolinecolor": "#EBF0F8"
                        },
                        "yaxis": {
                            "backgroundcolor": "white",
                            "gridcolor": "#DFE8F3",
                            "gridwidth": 2,
                            "linecolor": "#EBF0F8",
                            "showbackground": true,
                            "ticks": "",
                            "zerolinecolor": "#EBF0F8"
                        },
                        "zaxis": {
                            "backgroundcolor": "white",
                            "gridcolor": "#DFE8F3",
                            "gridwidth": 2,
                            "linecolor": "#EBF0F8",
                            "showbackground": true,
                            "ticks": "",
                            "zerolinecolor": "#EBF0F8"
                        }
                    },
                    "shapedefaults": {
                        "line": {
                            "color": "#2a3f5f"
                        }
                    },
                    "ternary": {
                        "aaxis": {
                            "gridcolor": "#DFE8F3",
                            "linecolor": "#A2B1C6",
                            "ticks": ""
                        },
                        "baxis": {
                            "gridcolor": "#DFE8F3",
                            "linecolor": "#A2B1C6",
                            "ticks": ""
                        },
                        "bgcolor": "white",
                        "caxis": {
                            "gridcolor": "#DFE8F3",
                            "linecolor": "#A2B1C6",
                            "ticks": ""
                        }
                    },
                    "title": {
                        "x": 0.05
                    },
                    "xaxis": {
                        "automargin": true,
                        "gridcolor": "#edeeee",
                        "gridwidth": 0.5,
                        "linecolor": "#EBF0F8",
                        "ticks": "",
                        "title": {
                            "standoff": 15
                        },
                        "zerolinecolor": "#edeeee",
                        "zerolinewidth": 2
                    },
                    "yaxis": {
                        "automargin": true,
                        "gridcolor": "#edeeee",
                        "gridwidth": 0.5,
                        "linecolor": "#EBF0F8",
                        "ticks": "",
                        "title": {
                            "standoff": 15
                        },
                        "zerolinecolor": "#edeeee",
                        "zerolinewidth": 2
                    }
                }
            }

            if (trigger == "themeToggle") {
                if (themeToggle) {
                    console.log("themeToggle_light");
                    new_fig['layout']['template'] = _light
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
                    new_fig['layout']['template']['layout'] = _dark
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
            return { 'data': new_fig['data'], 'layout': new_fig['layout'] };
        }
    }
});