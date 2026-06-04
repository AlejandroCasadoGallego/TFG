import reflex as rx

class ExcalidrawComponent(rx.Component):
    tag = "ExcalidrawWrapper"

    on_diagram_change: rx.EventHandler[lambda elements: [elements]]

    initial_data: rx.Var[str]

    def _get_imports(self):
        return {
            "@excalidraw/excalidraw": [
                rx.ImportVar(tag="Excalidraw"),
                rx.ImportVar(tag="exportToSvg"),
                rx.ImportVar(tag="serializeAsJSON"),
            ],
            "react": [rx.ImportVar(tag="useMemo"), rx.ImportVar(tag="useRef")],
        }

    def _get_custom_code(self) -> str:
        return """
import '@excalidraw/excalidraw/index.css';

const parseInitialExcalidrawData = (rawData) => {
    if (!rawData || typeof rawData !== 'string') {
        return null;
    }

    try {
        const parsed = JSON.parse(rawData);
        if (parsed && parsed.format === 'excalidraw-response' && parsed.scene) {
            return parsed.scene;
        }
        if (parsed && Array.isArray(parsed.elements)) {
            return parsed;
        }
    } catch (error) {
        return null;
    }

    return null;
};

if (typeof document !== 'undefined' && !document.head.querySelector('#patternlab-excalidraw-ui')) {
    const style = document.createElement('style');
    style.id = 'patternlab-excalidraw-ui';
    style.textContent = `
        .patternlab-excalidraw [aria-label="Library"],
        .patternlab-excalidraw [aria-label="Biblioteca"],
        .patternlab-excalidraw [title="Library"],
        .patternlab-excalidraw [title="Biblioteca"],
        .patternlab-excalidraw [data-testid="toolbar-library"],
        .patternlab-excalidraw [aria-label="Help"],
        .patternlab-excalidraw [aria-label="Ayuda"],
        .patternlab-excalidraw [title="Help"],
        .patternlab-excalidraw [title="Ayuda"],
        .patternlab-excalidraw [data-testid="help-menu"],
        .patternlab-excalidraw [data-testid="main-menu-trigger"],
        .patternlab-excalidraw [title^="Insert image"],
        .patternlab-excalidraw [title^="Insertar imagen"],
        .patternlab-excalidraw .App-toolbar__extra-tools-trigger,
        .patternlab-excalidraw [title="More tools"],
        .patternlab-excalidraw [title="Más herramientas"] {
            display: none !important;
        }
    `;
    document.head.appendChild(style);
}

const ExcalidrawWrapper = (props) => {
    const handler = props.on_diagram_change || props.onDiagramChange;
    const timeoutRef = useRef(null);
    const initData = props.initial_data || props.initialData || "";
    const initialScene = useMemo(() => parseInitialExcalidrawData(initData), [initData]);

    const emitDiagramChange = async (elements, appState, files) => {
        if (!handler) {
            return;
        }

        const visibleElements = (elements || []).filter((element) => !element.isDeleted);
        if (visibleElements.length === 0) {
            handler("");
            return;
        }

        try {
            const exportAppState = {
                ...appState,
                exportBackground: true,
                viewBackgroundColor: appState?.viewBackgroundColor || '#ffffff',
            };
            const svg = await exportToSvg({
                elements: visibleElements,
                appState: exportAppState,
                files: files || {},
            });
            const sceneJson = serializeAsJSON(elements || [], appState || {}, files || {}, 'local');
            handler(JSON.stringify({
                format: 'excalidraw-response',
                version: 1,
                svg: svg.outerHTML,
                scene: JSON.parse(sceneJson),
            }));
        } catch (error) {
            console.error('Error generating Excalidraw response', error);
        }
    };

    return (
        <div className="patternlab-excalidraw" style={{ width: '100%', height: '100%' }}>
            <Excalidraw
                initialData={initialScene || undefined}
                onChange={(elements, appState, files) => {
                    clearTimeout(timeoutRef.current);
                    timeoutRef.current = setTimeout(() => {
                        emitDiagramChange(elements, appState, files);
                    }, 800);
                }}
                langCode="es"
                theme="light"
                aiEnabled={false}
                UIOptions={{
                    canvasActions: {
                        export: false,
                        loadScene: false,
                        saveToActiveFile: false,
                        toggleTheme: false,
                    },
                }}
            />
        </div>
    );
};
"""

def diagram_board(**kwargs):
    return ExcalidrawComponent.create(**kwargs)
