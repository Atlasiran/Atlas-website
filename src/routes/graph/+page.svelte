<script lang="ts">
    import Sigma from "sigma";
    import Graph from "graphology";
    import { onMount } from "svelte";
    import { Button } from "$lib/components/ui/button/index";
    import Minus from "lucide-svelte/icons/minus";
    import Plus from "lucide-svelte/icons/plus";
    import ForceAtlas2 from "graphology-layout-forceatlas2";
    import { Play } from "lucide-svelte";
    import ShowNodeBar from "@/components/ShowNodeBar.svelte";
    import { base } from "$app/paths";

    let container: HTMLElement;
    let renderer: Sigma;
    let draggedNode: string | null = null;

    let selectTimeout: any = null;
    let isSideOpen = false;

    const state = {
        nodeHighlighted: false,
        hoveredNode: undefined,
        hoveredNeighbors: new Set<string>(),
    };

    let _subgraph;

    const zoomIn = () => {
        if (renderer) {
            const camera = renderer.getCamera();
            const currentRatio = camera.getState().ratio;
            camera.animate({ ratio: currentRatio / 1.5 }, { duration: 300 });
        }
    };

    const zoomOut = () => {
        if (renderer) {
            const camera = renderer.getCamera();
            const currentRatio = camera.getState().ratio;
            camera.animate({ ratio: currentRatio * 1.5 }, { duration: 300 });
        }
    };

    const runForceLayout = () => {
        if (renderer) {
            const graph = renderer.getGraph();
            const sensibleSettings = ForceAtlas2.inferSettings(graph);

            // Apply ForceAtlas2 layout
            ForceAtlas2.assign(graph, {
                iterations: 20,
                settings: sensibleSettings,
            });
            // Optionally, refresh the renderer to see the new positions immediately
            renderer.refresh();
        }
    };

    function setHoveredNode(node) {
        if (node) {
            state.hoveredNode = node;
            state.hoveredNeighbors = new Set(
                renderer.getGraph().neighbors(node),
            );
        } else {
            state.hoveredNode = undefined;
            state.hoveredNeighbors = new Set();
        }
        renderer.refresh({ skipIndexation: true });
    }

    function setDraggedNode(node: string | null) {
        draggedNode = node;
        if (node) {
            state.nodeHighlighted = true;
            state.hoveredNeighbors = new Set(
                renderer.getGraph().neighbors(node),
            );
        } else {
            state.nodeHighlighted = false;
            state.hoveredNeighbors = new Set();
        }
    }

    async function drawGraph(gexf) {
        const { parse } = await import("graphology-gexf/browser");
        const graph = parse(Graph, gexf);

        renderer = new Sigma(graph, container, {
            minCameraRatio: 0.1,
            maxCameraRatio: 10,
            defaultNodeType: "circle",
            defaultNodeColor: "#ccc",
        });

        renderer.on("downNode", (e) => {
            setDraggedNode(e.node);
            renderer.getGraph().setNodeAttribute(e.node, "highlighted", true);
            // disable graph dragging
            renderer.getCamera().disable();
            // highlight the node and its neighbors in the graph
            renderer.getGraph().forEachNeighbor(e.node, (neighbor) => {
                renderer
                    .getGraph()
                    .setNodeAttribute(neighbor, "highlighted-neighbor", true);
            });

            selectTimeout = setTimeout(() => {
                selectTimeout = null;
                isSideOpen = true;

                _subgraph = [];
                const data = renderer.getGraph().getNodeAttributes(e.node);
                _subgraph.push(data);

                renderer.getGraph().forEachNeighbor(e.node, (neighbor) => {
                    const data = renderer.getGraph().getNodeAttributes(neighbor);
                    _subgraph.push(data);
                });
            }, 200);
        });

        renderer.getMouseCaptor().on("mousemove", (e) => {
            if (!draggedNode) return;
            if (selectTimeout) {
                clearTimeout(selectTimeout);
            }
            const pos = renderer.viewportToGraph({ x: e.x, y: e.y });
            renderer.getGraph().setNodeAttribute(draggedNode, "x", pos.x);
            renderer.getGraph().setNodeAttribute(draggedNode, "y", pos.y);
        });

        renderer.getMouseCaptor().on("mouseup", () => {
            if (draggedNode) {
                // Remove highlight attributes
                renderer
                    .getGraph()
                    .removeNodeAttribute(draggedNode, "highlighted");
                renderer.getGraph().forEachNeighbor(draggedNode, (neighbor) => {
                    renderer
                        .getGraph()
                        .removeNodeAttribute(neighbor, "highlighted-neighbor");
                });
                setDraggedNode(null);
                // enable graph dragging
                renderer.getCamera().enable();
            }
        });

        renderer.getMouseCaptor().on("mousedown", () => {
            if (!renderer.getCustomBBox())
                renderer.setCustomBBox(renderer.getBBox());
        });

        // Handle node hover event
        renderer.on("enterNode", ({ node }) => {
            if (draggedNode) return;
            setHoveredNode(node);
        });
        renderer.on("leaveNode", () => {
            if (draggedNode) return;
            setHoveredNode(undefined);
        });

        // Node reducer
        renderer.setSetting("nodeReducer", (node, data) => {
            const res = { ...data };
            if (
                state.hoveredNode &&
                !state.hoveredNeighbors.has(node) &&
                state.hoveredNode !== node
            ) {
                res.label = "";
                res.opacity = 0.1;
                res.color = "#ccc";
            } else if (state.hoveredNode === node) {
                res.color = "#ff0000";
            } else if (state.hoveredNeighbors.has(node)) {
                res.color = "#ff0000"; // Highlight neighbor in red
            } else {
                res.opacity = 0.1;
            }

            if (data["@labels"] === "Country") {
                res.size = 15;
                // indigo
                res.color = "#7274f1";
            } else if (data["@labels"] === "Organization") {
                res.size = 5;
                // green
                res.color = "#34d399";
            } else if (data["@labels"] === "Political Party") {
                res.size = 5;
                // orange
                res.color = "#f97316";
            } else {
                res.size = 5;
            }

            // hover coursor
            res.styles = "cursor: pointer";

            return res;
        });

        // Edge reducer
        renderer.setSetting("edgeReducer", (edge, data) => {
            const res = { ...data };

            if (
                state.hoveredNode &&
                !renderer.getGraph().hasExtremity(edge, state.hoveredNode)
            ) {
                res.color = "#ccc";
            } else if (state.hoveredNode) {
                res.color = "red";
            }

            return res;
        });

        runForceLayout();
    }

    function closePanel() {
        isSideOpen = false;
    }

    onMount(async () => {
        const res = await fetch(`${base}/test.gexf`);
        const gexf = await res.text();
        await drawGraph(gexf);
    });
</script>

<!-- Graph container -->
<div class="graph-view">
    <div
        class="sidebar flex flex-col"
        style="width:{isSideOpen ? '400px' : '0px'}"
    >
        <ShowNodeBar {closePanel} subgraph={_subgraph} />
    </div>

    <div
        dir="ltr"
        bind:this={container}
        class="graph-container"
        style="width:{isSideOpen ? 'calc(100vw - 400px)' : '100vw'}"
    >
        <!-- Control Buttons -->
        <div class="zoom-controls">
            <Button variant="outline" size="icon" on:click={zoomIn}>
                <Plus class="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" on:click={zoomOut}>
                <Minus class="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" on:click={runForceLayout}>
                <!-- play -->
                <Play class="h-4 w-4" />
            </Button>
            <!-- Added Force Layout Button -->
        </div>
    </div>
</div>

<!-- Styles -->
<style>
    .graph-container {
        height: 100%;
        position: relative;
        background-color: #fff;
        background-image: radial-gradient(#cccbcb 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .sidebar {
        height: 100%;
        background-color: #f9fafb;
    }
    .graph-view {
        width: 100vw;
        display: flex;
        flex-direction: row;
        height: calc(100vh - 50px);
    }

    .zoom-controls {
        position: absolute;
        bottom: 16px;
        right: 16px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        z-index: 20;
    }

    /* Add custom node styles */
    .graph-container .highlighted {
        fill: #ff0000; /* red color for highlighted nodes */
        stroke: #ff0000;
    }

    .graph-container .highlighted-neighbor {
        fill: #ffa500; /* orange color for highlighted neighbors */
        stroke: #ffa500;
    }
</style>
