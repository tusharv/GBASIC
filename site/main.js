"use strict";

// These controls switch static screenshots and instructions. BASIC runs in the local app.
for (const group of document.querySelectorAll("[data-tab-group]")) {
  const tabs = [...group.querySelectorAll('[role="tab"]')];
  const select = (chosen, focus = false) => {
    for (const tab of tabs) {
      const active = tab === chosen;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(tab.getAttribute("aria-controls"));
      panel.hidden = !active;
      panel.tabIndex = 0;
    }
    if (focus) chosen.focus();
  };
  for (const tab of tabs) {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (event) => {
      let index = tabs.indexOf(tab);
      if (event.key === "ArrowRight") index = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") index = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") index = 0;
      else if (event.key === "End") index = tabs.length - 1;
      else return;
      event.preventDefault();
      select(tabs[index], true);
    });
  }
  select(tabs.find((tab) => tab.getAttribute("aria-selected") === "true") || tabs[0]);
}

for (const button of document.querySelectorAll("[data-copy]")) {
  button.addEventListener("click", async () => {
    const code = document.getElementById(button.dataset.copy);
    const status = document.getElementById("copy-status");
    try {
      if (!navigator.clipboard) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = "Copied!";
      status.textContent = "Installation commands copied.";
      setTimeout(() => { button.textContent = "Copy commands"; }, 2000);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = "Commands selected. Press Ctrl+C or Cmd+C to copy.";
    }
  });
}
