import { describe, expect, it } from "vitest";
import { renderMarkdown } from "../../../src/features/standup/renderMarkdown";

describe("renderMarkdown", () => {
  it("emits three H3 sections with trailing newline", () => {
    const md = renderMarkdown("y", "t", "b");
    expect(md).toBe("### Yesterday\ny\n\n### Today\nt\n\n### Blockers\nb\n");
  });

  it("renders Blockers: None when blockers empty", () => {
    const md = renderMarkdown("y", "t", "   ");
    expect(md).toContain("### Blockers\nNone");
  });

  it("renders (none) placeholder when yesterday empty", () => {
    const md = renderMarkdown("", "t", "b");
    expect(md).toContain("### Yesterday\n(none)");
  });

  it("trims leading/trailing whitespace on all fields", () => {
    const md = renderMarkdown("  hello  ", "  world  ", "   ");
    expect(md).toBe("### Yesterday\nhello\n\n### Today\nworld\n\n### Blockers\nNone\n");
  });

  it("preserves internal whitespace and newlines", () => {
    const input = "- a\n- b\n\nnext line";
    const md = renderMarkdown(input, "t", "");
    expect(md).toContain(`### Yesterday\n${input}`);
  });

  it("is deterministic — identical inputs produce identical output", () => {
    expect(renderMarkdown("a", "b", "c")).toBe(renderMarkdown("a", "b", "c"));
  });
});
