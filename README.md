# PHYSRUM-GNN: Aster City routing simulation

**Start the visual dashboard (Python 3.10+, no packages or internet):**

```bash
python app.py
```

The browser should open automatically at **http://127.0.0.1:8765**. If it does not, paste that address into your browser. Keep the terminal open while using the dashboard; Ctrl+C stops it. This is a **fictional, medium-size city**, with a river, three bridges, parks, landmarks, districts, 166 intersections, and 288 road segments. It is deliberately separate from the offline Guwahati CLI experiment below.

The dashboard opens with an example start and destination already selected. Press **Block central bridge** to create a recoverable disruption on the original route. Alternatively, press **Pick start** and **Pick destination** to click any two intersections; press **Pick roads** to close multiple roads by clicking their segments. Clicking a blocked road reopens it. You can also enter comma-separated road IDs, clear closures, or reset the trip. Press **Run simulation**: Physarum runs first and displays its recovered path on the main map, followed by Dijkstra. Two report cards then appear side by side with separate route maps, estimated drive time, and measured rerouting latency. A visual pause makes the sequence easy to follow; it is **not** included in measured latency. If closures disconnect the destination, the cards say unreachable.

The browser and routing API both run locally. They use `data/custom_city.json` and Python's standard library and do not fetch online maps. `python scripts/build_city.py` deterministically regenerates the fictional city. The dashboard compares Physarum and Dijkstra, as requested. The earlier Guwahati CLI benchmark still includes the GNN and generates CSVs and maps; it is independent of this fictional-city dashboard.

## Optional CLI benchmark

```bash
python main.py
```

The demo blocks a simulated road on the original Maligaon-Kamakhya route and runs Dijkstra, warm-start Physarum, and Physarum-GNN on that same closure. Open `output/maligaon_before.svg` and `output/maligaon_after.svg` for the original route and Physarum detour. `output/maligaon_after_dijkstra.svg` and `output/maligaon_after_gnn.svg` show the other paths. The command also runs Jorabat and Panikhaiti scenarios, saves equivalent maps and full paths in `output/*_routes.json`, and writes `output/benchmark.csv` plus `output/model_evaluation.csv`.

## Block your own road

```bash
python main.py --scenario maligaon --list-route
python main.py --scenario maligaon --close-edge 14255
```

The first command lists local road IDs along the original route. Use one of those IDs in the second command to ensure the original route breaks. Alternatively, run `python main.py --scenario maligaon --interactive` to list IDs and enter one or several comma-separated IDs at a prompt. For multiple closures use `--close-edge 14255,14256`. The IDs refer to segments in the bundled graph, not OSM way IDs. Other choices: `--scenario jorabat`, `--scenario panikhaiti`, or `--close-at 91.854,26.174` with `--scenario panikhaiti` to block the nearest road to a longitude and latitude.

Each method reports whether its path remains valid, estimated drive minutes, rerouting milliseconds, and a route preview. Complete ordered road IDs are in the CSV, and complete route coordinates and map filenames are in `output/maligaon_custom_14255_routes.json` for the example above. Open the corresponding `*_before.svg`, `*_after.svg` (Physarum), `*_after_dijkstra.svg`, and `*_after_gnn.svg`. Custom outputs have distinct filenames and preserve the default maps. An unreachable destination produces an empty path and blank estimated drive time. A closure off the original route can leave the fixed route valid.

## Measured comparison

The fixed pre-disaster route is computed before the closure and validated afterward; zero rerouting time means it never reroutes. Dijkstra recomputes the shortest route with the road removed. Physarum uses pre-event conductivity, solves nodal pressures, computes flux and reinforces used edges while others decay; it then extracts a directed path. The lightweight one-hop GNN modifies its initial conductivity using features and weights learned from simulated closures in separate corridors. Post-closure latency includes GNN inference, Physarum iterations, and path extraction, but excludes offline training and pre-event preparation.

One run on this machine, with simulated blockade 14255:

| Method | Valid after closure | Estimated drive | Rerouting latency |
| --- | --- | ---: | ---: |
| Fixed pre-disaster | No | unavailable | 0 ms |
| Dijkstra rerun | Yes | 5.310 min | 1.072 ms |
| Physarum | Yes | 5.310 min | 5,467.157 ms |
| Physarum-GNN | Yes | 5.310 min | 5,649.875 ms |

Timings vary by machine. Dijkstra is substantially faster in this experiment; the GNN did not improve validity or drive time. The evaluation CSV reports recall of the held-out bypass edges among the highest-scoring 5% GNN predictions. The results do not support a claim that conventional shortest-path rerouting is static or inferior.

## Data and limitations

`data/guwahati_roads.json` bundles 91,923 vertices and 87,662 OSM-derived road segments, including 5,904 marked one-way. Roads and geometries were extracted from bundled OpenFreeMap zoom-14 vector tiles; `python scripts/build_tiles.py` rebuilds the JSON from the cached tiles. Tile generalization can omit minor roads or misconnect junctions, and turn restrictions are unavailable. Endpoint snapping can move the scenario endpoints away from the approximate corridor anchors; check snapped coordinates in each `*_routes.json`. The Panikhaiti experiment covers an eastbound approach toward Chandrapur, not Chandrapur itself. The pressure solver relaxes an undirected electrical network; route extraction enforces one-way roads. Road speeds are assumed from class, without traffic; terrain and flood features are simulated proxies, not measured elevation or flood data. The closures are simulated, not observed events. This is an offline routing experiment and not operational emergency guidance.

Retrain with `python main.py --train`; run tests with `python -m unittest discover -s tests -v`. Python standard library only. Road data: [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL, via [OpenFreeMap](https://openfreemap.org/) vector tiles.
