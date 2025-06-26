import { test, expect, WebSocketFrame } from '@playwright/test';

/**
 * Launches the app, opens the settings drawer, toggles the
 * "Force tools on long queries" switch and verifies that the
 * WebSocket payload reflects the change by updating the
 * `force_tool` value.
 */

test('force_tool toggle updates server via websocket', async ({ page }) => {
  // Capture the first WebSocket connection from the page
  const wsPromise = page.waitForEvent('websocket');
  await page.goto('/');
  const ws = await wsPromise;

  const frames: WebSocketFrame[] = [];
  ws.on('framesent', frame => frames.push(frame));

  // Open the settings drawer
  await page.getByRole('button', { name: /settings/i }).click();

  const toggle = page.getByLabel('Force tools on long queries');

  // Disable the setting
  await toggle.click();
  const payloadOff = frames
    .map(f => {
      try {
        return JSON.parse(f.payload.toString());
      } catch {
        return undefined;
      }
    })
    .find(m => m && m.content && m.content.tool_args);

  expect(payloadOff.content.tool_args.force_tool).toBe(false);
  frames.length = 0;

  // Enable the setting again
  await toggle.click();
  const payloadOn = frames
    .map(f => {
      try {
        return JSON.parse(f.payload.toString());
      } catch {
        return undefined;
      }
    })
    .find(m => m && m.content && m.content.tool_args);

  expect(payloadOn.content.tool_args.force_tool).toBe(true);
});
