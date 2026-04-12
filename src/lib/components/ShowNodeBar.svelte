<script>
    import ChevronRight from "lucide-svelte/icons/chevron-right";
    import { Button } from "$lib/components/ui/button/index";
    import Sigma from "sigma";
    import { Graph } from "graphology";
    import { onMount } from "svelte";
    import ForceAtlas2 from "graphology-layout-forceatlas2";

    export let subgraph;
    export let closePanel = () => {};
    let container;
    let _initialized = false;
    let renderer;

    async function drawGraph(_subgraph) {
        if (!_subgraph) return;
        if (renderer) {
            renderer.kill();
        }

        // turn node array data to subgraph
        const graph = new Graph();
        _subgraph.map((node) => {
            graph.addNode(node["@id"], {
                label: node["label"],
                attributes: node,
                x: Math.random() * 1000,
                y: Math.random() * 1000,
                size: 20,
            });
        });
        _subgraph.map((node) => {
            graph.addEdge(_subgraph[0]["@id"], node["@id"]);
        });

        // const graph = Sigma.parsers.json(graphـdata, {
        //     container: "container",
        //     settings: {
        //         defaultNodeColor: "#ec5148",
        //     },
        // });

        renderer = new Sigma(graph, container, {
            minCameraRatio: 0.1,
            maxCameraRatio: 10,
            defaultNodeType: "circle",
            defaultNodeColor: "#ccc",
        });

        // Node reducer
        renderer.setSetting("nodeReducer", (node, data) => {
            const res = { ...data };

            if (data["@labels"] === "Country") {
                res.size = 15;
                // indigo
                res.color = "#7274f1";
            } else if (data["@labels"] === "Organization") {
                res.size = 15;
                // green
                res.color = "#34d399";
            } else if (data["@labels"] === "Political Party") {
                res.size = 15;
                // orange
                res.color = "#f97316";
            } else {
                res.size = 15;
            }

            // hover coursor
            res.styles = "cursor: pointer";

            return res;
        });

        if (renderer) {
            const graph = renderer.getGraph();
            const sensibleSettings = ForceAtlas2.inferSettings(graph);

            // Apply ForceAtlas2 layout
            ForceAtlas2.assign(graph, {
                iterations: 200,
                settings: {
                    ...sensibleSettings,
                    scalingRatio: 270,
                    strongGravityMode: false,
                },
            });
            // Optionally, refresh the renderer to see the new positions immediately
            renderer.refresh();
        }
    }

    onMount(() => {
        drawGraph(subgraph);
        _initialized = true;
    });

    $: _initialized && drawGraph(subgraph);
</script>

<div class="flex-grow pt-4">
    <div class="">
        <h1 class="text-4xl font-bold text-[#1E3A6B] p-4 pb-8">اطلاعات گره</h1>

        <div bind:this={container} class="graph-container"></div>
    </div>
</div>
<div class="flex flex-row justify-end w-full">
    <Button variant="ghost" size="icon" on:click={closePanel}>
        <ChevronRight class="text-[rgba(30,58,107,0.56)]" />
    </Button>
</div>

<style>
    .graph-container {
        height: 400px;
        width: 400px;
        background-color: #F4F6F7;
        direction: ltr;
    }
</style>
