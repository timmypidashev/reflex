import { Fragment, useEffect } from "react"
import { useThemeContext, themePropDefs } from "@radix-ui/themes"


function reflexRadixTheme(context) {
    const {
        appearance,
        accentColor,
        grayColor,
        panelBackground,
        radius,
        scaling,
    } = context;
    const theme = {
        appearance: appearance === themePropDefs.appearance.default ? undefined : appearance,
        accent_color: accentColor === themePropDefs.accentColor.default ? undefined : accentColor,
        gray_color: grayColor === themePropDefs.grayColor.default ? undefined : grayColor,
        panel_background:
          panelBackground === themePropDefs.panelBackground.default ? undefined : panelBackground,
        radius: radius === themePropDefs.radius.default ? undefined : radius,
        scaling: scaling === themePropDefs.scaling.default ? undefined : scaling,
    };

    const props = Object.keys(theme)
        .filter((key) => theme[key] !== undefined)
        .map((key) => `${key}="${theme[key]}"`)
        .join(' ');

    return props ? `rx.theme(${props})` : 'rx.theme()';
}


export default function ThemePanelCopyButtonOverride() {
    const context = useThemeContext();
    useEffect(() => {
        const buttonText = 'Copy Theme';
        const buttons = document.querySelectorAll('button');
        let copy_theme_button = undefined 
        console.log(JSON.stringify(context))

        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].textContent.includes(buttonText)) {
                // Button found
                copy_theme_button = buttons[i]
                break;
            }
        }

        async function fix_theme_clipboard() {
            navigator.clipboard.writeText(reflexRadixTheme(context))
        }

        function click_handler() {
            window.setTimeout(fix_theme_clipboard, 100)
        }

        if (copy_theme_button) {
            copy_theme_button.addEventListener('click', click_handler)
            return () => copy_theme_button.removeEventListener('click', click_handler)
        }
    }, []);

    return <Fragment />
}