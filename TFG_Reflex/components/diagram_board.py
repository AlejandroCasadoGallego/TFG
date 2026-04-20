import reflex as rx

class TldrawComponent(rx.Component):
    tag = "TldrawWrapper"

    on_diagram_change: rx.EventHandler[lambda elements: [elements]]

    initial_data: rx.Var[str]

    def _get_imports(self):
        return {
            "tldraw": [rx.ImportVar(tag="Tldraw")],
            "react": [rx.ImportVar(tag="useRef"), rx.ImportVar(tag="useEffect")]
        }

    def _get_custom_code(self) -> str:
        return """
import 'tldraw/tldraw.css';

const hiddenUiStyle = document.createElement('style');
hiddenUiStyle.textContent = `
    .tlui-menu-zone { display: none !important; }
    .tlui-navigation-zone { display: none !important; }
    .tlui-help-menu { display: none !important; }
    a[href*="tldraw.dev"] { display: none !important; }
    .tlui-watermark_SEE-LICENSE { display: none !important; }
    [class*="watermark"] { display: none !important; }
`;
if (!document.head.querySelector('#tldraw-hide-ui')) {
    hiddenUiStyle.id = 'tldraw-hide-ui';
    document.head.appendChild(hiddenUiStyle);
}

const TldrawWrapper = (props) => {
    const handler = props.on_diagram_change || props.onDiagramChange;
    const editorRef = useRef(null);
    const loadedRef = useRef(false);
    const initData = props.initial_data || props.initialData || "";

    useEffect(() => {
        // SVG loading is not supported, start fresh every time
    }, [initData]);

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <Tldraw 
                hideUi={false}
                onMount={(editor) => {
                    editorRef.current = editor;

                    let timeout;
                    editor.store.listen(() => {
                        clearTimeout(timeout);
                        timeout = setTimeout(async () => {
                            if (handler) {
                                const shapeIds = Array.from(editor.getCurrentPageShapeIds());
                                if (shapeIds.length > 0) {
                                    try {
                                        const result = await editor.getSvgString(shapeIds, { background: true });
                                        if (result && result.svg) {
                                            handler(result.svg);
                                        }
                                    } catch (e) {
                                        console.error("Error generating SVG", e);
                                    }
                                } else {
                                    handler("");
                                }
                            }
                        }, 1000);
                    }, { scope: 'document', source: 'user' });
                }}
            />
        </div>
    );
};
"""

def diagram_board(**kwargs):
    return TldrawComponent.create(
        **kwargs
    )
