import { c as openBlock, h as createElementBlock, j as createBaseVNode, d as defineComponent, q as computed, fM as useTemplateRef, o as onMounted, fX as useFavicon, i as createVNode, n as normalizeClass, l as unref, e as createBlock, f as createCommentVNode, t as toDisplayString, s as renderSlot, aa as useCssModule, _ as _export_sfc } from "./index-BfLzQZy8.js";
const _hoisted_1$1 = {
  xmlns: "http://www.w3.org/2000/svg",
  width: "50",
  height: "30"
};
function render$1(_ctx, _cache) {
  return openBlock(), createElementBlock("svg", _hoisted_1$1, _cache[0] || (_cache[0] = [
    createBaseVNode("path", {fill: "#EA4B71","fill-rule": "evenodd",d: " ","clip-rule": "evenodd"}, null, -1),createBaseVNode("path", { d: " " })
  ]));
}
const LogoIcon = { render: render$1 };
const _hoisted_1 = {
  width: "26",
  height: "30"
};
function render(_ctx, _cache) {
  return openBlock(), createElementBlock("svg", _hoisted_1, _cache[0] || (_cache[0] = [
    createBaseVNode("g", { fill: "#101330" }, [
      createBaseVNode("path", {
        "fill-rule": "evenodd",
        d: " ",
        "clip-rule": "evenodd"
      }),
      createBaseVNode("path", { d: " " })
    ], -1)
  ]));
}
const LogoText = { render };
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "Logo",
  props: {
    location: {},
    collapsed: { type: Boolean },
    releaseChannel: {}
  },
  setup(__props) {
    const props = __props;
    const { location, releaseChannel } = props;
    const showReleaseChannelTag = computed(() => {
      if (releaseChannel === "stable") return false;
      if (location === "authView") return true;
      return !props.collapsed;
    });
    const showLogoText = computed(() => {
      if (location === "authView") return true;
      return !props.collapsed;
    });
    const $style = useCssModule();
    const containerClasses = computed(() => {
      if (location === "authView") {
        return [$style.logoContainer, $style.authView];
      }
      return [
        $style.logoContainer,
        $style.sidebar,
        props.collapsed ? $style.sidebarCollapsed : $style.sidebarExpanded
      ];
    });
    const svg = useTemplateRef("logo");
    onMounted(() => {
      if (releaseChannel === "stable" || !("createObjectURL" in URL)) return;
      const logoEl = svg.value.$el;
      const logoColor = releaseChannel === "dev" ? "#838383" : "#E9984B";
      logoEl.querySelector("path")?.setAttribute("fill", logoColor);
      const blob = new Blob([logoEl.outerHTML], { type: "image/svg+xml" });
      useFavicon(URL.createObjectURL(blob));
    });
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("div", {
        class: normalizeClass(containerClasses.value),
        "data-test-id": "n8n-logo"
      }, [
        createVNode(unref(LogoIcon), {
          class: normalizeClass(unref($style).logo),
          ref: "logo"
        }, null, 8, ["class"]),
        showLogoText.value ? (openBlock(), createBlock(unref(LogoText), {
          key: 0,
          class: normalizeClass(unref($style).logoText)
        }, null, 8, ["class"])) : createCommentVNode("", true),
        showReleaseChannelTag.value ? (openBlock(), createElementBlock("div", {
          key: 1,
          size: "small",
          round: "",
          class: normalizeClass(unref($style).releaseChannelTag)
        }, toDisplayString(unref(releaseChannel)), 3)) : createCommentVNode("", true),
        renderSlot(_ctx.$slots, "default")
      ], 2);
    };
  }
});
const logoContainer = "_logoContainer_1p61r_123";
const logoText = "_logoText_1p61r_128";
const releaseChannelTag = "_releaseChannelTag_1p61r_135";
const authView = "_authView_1p61r_149";
const sidebar = "_sidebar_1p61r_154";
const sidebarExpanded = "_sidebarExpanded_1p61r_158";
const logo = "_logo_1p61r_123";
const sidebarCollapsed = "_sidebarCollapsed_1p61r_162";
const style0 = {
  logoContainer,
  logoText,
  releaseChannelTag,
  authView,
  sidebar,
  sidebarExpanded,
  logo,
  sidebarCollapsed
};
const cssModules = {
  "$style": style0
};
const Logo = /* @__PURE__ */ _export_sfc(_sfc_main, [["__cssModules", cssModules]]);
export {
  Logo as L
};
