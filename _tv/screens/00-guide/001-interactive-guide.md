---
id: 001-interactive-guide
title: CCTV Interactive Guide & Sandbox
type: interactive
status: running
---
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            accentYellow: '#e0a23c',
            doneGreen: '#6f9e6a',
            blockedRed: '#c2683f'
          }
        }
      }
    }
  </script>
</head>
<body class="bg-slate-50 text-slate-800 p-4 font-sans h-full flex flex-col antialiased">
  <div class="mb-3 shrink-0">
    <h1 class="text-base font-bold text-slate-900 flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-accentYellow animate-pulse"></span>
      CCTV Interactive Guide & Playbook
    </h1>
    <p class="text-xs text-slate-500 mt-0.5">Build cards, set up screens, and copy code templates dynamically below.</p>
  </div>

  <!-- Navigation Tabs -->
  <div class="flex border-b border-slate-200 text-[11px] font-semibold mb-3 gap-0.5 shrink-0 overflow-x-auto whitespace-nowrap pb-1">
    <button onclick="switchTab('playground')" id="tab-playground" class="px-2.5 py-1.5 border-b-2 border-accentYellow text-slate-900 -mb-[2px] transition-all">1. Controls Sandbox</button>
    <button onclick="switchTab('charts')" id="tab-charts" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all">2. SVG Playground</button>
    <button onclick="switchTab('wizard-card')" id="tab-wizard-card" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all font-bold text-emerald-600">3. Card UI Wizard</button>
    <button onclick="switchTab('wizard-screen')" id="tab-wizard-screen" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all font-bold text-emerald-600">4. Screen Wizard</button>
    <button onclick="switchTab('cookbook')" id="tab-cookbook" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all">5. Code Templates</button>
    <button onclick="switchTab('guide')" id="tab-guide" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all">6. Full User Guide</button>
    <button onclick="switchTab('simulator')" id="tab-simulator" class="px-2.5 py-1.5 border-b-2 border-transparent text-slate-500 hover:text-slate-900 -mb-[2px] transition-all font-bold text-indigo-600">7. Pipeline Simulator</button>
  </div>

  <!-- Tab 1: Playground -->
  <div id="content-playground" class="flex-1 flex flex-col gap-3 min-h-0">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-1 min-h-0 overflow-auto">
      <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-2.5">
        <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Sandbox Controls</h2>
        
        <div>
          <label class="block text-[11px] font-bold text-slate-600 mb-1">Choice Buttons</label>
          <div class="flex gap-2">
            <button onclick="updateSelection('Approve')" class="flex-1 py-1.5 text-xs font-medium border border-slate-200 rounded-md hover:bg-slate-50 active:bg-slate-100 transition-colors">Approve</button>
            <button onclick="updateSelection('Reject')" class="flex-1 py-1.5 text-xs font-medium border border-slate-200 rounded-md hover:bg-slate-50 active:bg-slate-100 transition-colors">Reject</button>
          </div>
        </div>

        <div>
          <div class="flex justify-between text-[11px] font-bold text-slate-600 mb-0.5">
            <span>Range Slider</span>
            <span id="slider-txt" class="text-accentYellow font-bold">50%</span>
          </div>
          <input type="range" id="sandbox-slider" min="0" max="100" value="50" oninput="updateSlider(this.value)" class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer">
        </div>

        <div>
          <label class="block text-[11px] font-bold text-slate-600 mb-0.5">Radio Selectors</label>
          <div class="flex gap-4 text-xs">
            <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" name="priority" value="low" onclick="updateRadio(this.value)"> Low</label>
            <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" name="priority" value="medium" checked onclick="updateRadio(this.value)"> Medium</label>
            <label class="flex items-center gap-1.5 cursor-pointer"><input type="radio" name="priority" value="high" onclick="updateRadio(this.value)"> High</label>
          </div>
        </div>
      </div>

      <div class="bg-slate-900 text-slate-300 p-3 rounded-lg flex flex-col font-mono text-[11px] shadow-sm justify-between">
        <div class="min-h-0 overflow-auto">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-2 border-b border-slate-800 pb-1">
            <span>Payload output preview</span>
            <span class="text-emerald-400 font-bold">LIVE</span>
          </div>
          <pre id="payload-preview" class="text-slate-100 leading-tight">{\n  "selection": "None",\n  "sliderValue": 50,\n  "priority": "medium"\n}</pre>
        </div>
        <div class="border-t border-slate-800 pt-2 mt-2 flex flex-col gap-1.5 shrink-0">
          <p class="text-[9px] text-slate-400">Submit this response back to the active stage response directory:</p>
          <button onclick="sendPayload()" class="w-full bg-accentYellow hover:bg-amber-500 text-slate-900 font-bold py-1.5 rounded text-xs transition-colors flex items-center justify-center gap-1">
            Submit response bridge
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Tab 2: Charts -->
  <div id="content-charts" class="flex-1 flex flex-col gap-3 min-h-0 hidden">
    <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-3 flex-1 min-h-0 overflow-auto">
      <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Interactive SVG Visualizer</h2>
      
      <div class="grid grid-cols-3 gap-3 shrink-0">
        <div>
          <label class="block text-[10px] font-bold text-slate-500 mb-0.5">BAR A (Accuracy)</label>
          <input type="range" min="10" max="100" value="75" oninput="updateChartBar('a', this.value)" class="w-full">
        </div>
        <div>
          <label class="block text-[10px] font-bold text-slate-500 mb-0.5">BAR B (Speed)</label>
          <input type="range" min="10" max="100" value="90" oninput="updateChartBar('b', this.value)" class="w-full">
        </div>
        <div>
          <label class="block text-[10px] font-bold text-slate-500 mb-0.5">BAR C (Safety)</label>
          <input type="range" min="10" max="100" value="55" oninput="updateChartBar('c', this.value)" class="w-full">
        </div>
      </div>

      <div class="flex-1 flex justify-center border-t border-slate-100 pt-3 min-h-0">
        <svg viewBox="0 0 200 100" class="w-full max-w-[260px] h-full">
          <line x1="10" y1="90" x2="190" y2="90" stroke="#cbd5e1" stroke-width="1.5"></line>
          
          <rect id="bar-a" x="25" y="30" width="30" height="60" fill="#e0a23c" rx="2" class="transition-all duration-150" />
          <text id="lbl-a" x="40" y="24" font-size="8" font-family="monospace" text-anchor="middle" font-weight="bold">75%</text>
          <text x="40" y="98" font-size="7" font-weight="bold" text-anchor="middle" fill="#64748b">Accuracy</text>
          
          <rect id="bar-b" x="85" y="18" width="30" height="72" fill="#6f9e6a" rx="2" class="transition-all duration-150" />
          <text id="lbl-b" x="100" y="12" font-size="8" font-family="monospace" text-anchor="middle" font-weight="bold">90%</text>
          <text x="100" y="98" font-size="7" font-weight="bold" text-anchor="middle" fill="#64748b">Speed</text>
          
          <rect id="bar-c" x="145" y="46" width="30" height="44" fill="#c2683f" rx="2" class="transition-all duration-150" />
          <text id="lbl-c" x="160" y="40" font-size="8" font-family="monospace" text-anchor="middle" font-weight="bold">55%</text>
          <text x="160" y="98" font-size="7" font-weight="bold" text-anchor="middle" fill="#64748b">Safety</text>
        </svg>
      </div>
      <p class="text-[9px] text-slate-400 text-center italic shrink-0">Drag sliders to adjust SVG bar heights and label positions dynamically.</p>
    </div>
  </div>

  <!-- Tab 3: Card UI Creator Wizard (New!) -->
  <div id="content-wizard-card" class="flex-1 flex flex-col gap-3 min-h-0 hidden">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-1 min-h-0 overflow-auto">
      <!-- Input Panel -->
      <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-2.5 overflow-y-auto">
        <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Card Configuration</h2>
        
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Screen Folder</label>
            <input type="text" id="wiz-card-screen" value="demo" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
          </div>
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Card Filename</label>
            <input type="text" id="wiz-card-id" value="002-checkpoint" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
          </div>
        </div>

        <div class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">Card Title</label>
          <input type="text" id="wiz-card-title" value="Pipeline Decision" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
        </div>

        <div class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">User Prompt Question</label>
          <input type="text" id="wiz-card-prompt" value="Select the path forward:" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
        </div>

        <div class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">UI Type</label>
          <select id="wiz-card-ui" onchange="onWizardUIChange(this.value)" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
            <option value="buttons">Buttons (Single Choice)</option>
            <option value="slider">Slider (Numeric Range)</option>
            <option value="radio">Radio Buttons</option>
            <option value="checkboxes">Checkboxes (Multiple Choice)</option>
            <option value="chart">SVG Bar Chart</option>
          </select>
        </div>

        <!-- Conditional fields -->
        <div id="wiz-options-container" class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">Button/Selection Choices (comma-separated)</label>
          <input type="text" id="wiz-card-options" value="Approve, Reject, Request revisions" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
        </div>

        <div id="wiz-slider-container" class="grid grid-cols-3 gap-2 text-xs hidden">
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Min</label>
            <input type="number" id="wiz-slider-min" value="0" class="w-full p-1 border rounded">
          </div>
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Max</label>
            <input type="number" id="wiz-slider-max" value="100" class="w-full p-1 border rounded">
          </div>
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Default</label>
            <input type="number" id="wiz-slider-def" value="50" class="w-full p-1 border rounded">
          </div>
        </div>

        <div id="wiz-chart-container" class="grid grid-cols-2 gap-2 text-xs hidden">
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Values (comma-separated)</label>
            <input type="text" id="wiz-chart-vals" value="70, 90, 55" class="w-full p-1 border rounded">
          </div>
          <div>
            <label class="block font-semibold text-slate-600 mb-0.5">Labels (comma-separated)</label>
            <input type="text" id="wiz-chart-lbls" value="Accuracy, Speed, Safety" class="w-full p-1 border rounded">
          </div>
        </div>

        <button onclick="generateWizardCard()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 rounded text-xs transition-colors shrink-0 mt-1">Generate Card Code</button>
      </div>

      <!-- Code Output -->
      <div class="bg-slate-900 p-3 rounded-lg flex flex-col font-mono text-[10px] shadow-sm justify-between min-h-0">
        <div class="flex-1 flex flex-col min-h-0">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-2 border-b border-slate-800 pb-1 shrink-0">
            <span>Generated Card Markup</span>
            <button onclick="copyCode('wiz-card-output')" class="text-emerald-400 font-bold hover:underline">Copy Code</button>
          </div>
          <textarea id="wiz-card-output" readonly class="flex-1 w-full bg-slate-950 text-slate-200 p-2 border border-slate-850 rounded resize-none outline-none leading-tight font-mono text-[10px] min-h-0"></textarea>
        </div>
        <div class="border-t border-slate-800 pt-2 mt-2 text-[9.5px] text-slate-400 shrink-0">
          Save this content to file: <code id="wiz-card-path" class="text-accentYellow">_tv/screens/demo/002-checkpoint.md</code>
        </div>
      </div>
    </div>
  </div>

  <!-- Tab 4: Pipeline Screen Creator Wizard (New!) -->
  <div id="content-wizard-screen" class="flex-1 flex flex-col gap-3 min-h-0 hidden">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-1 min-h-0 overflow-auto">
      <!-- Input Panel -->
      <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-3 overflow-y-auto">
        <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Pipeline Screen Setup Wizard</h2>
        
        <div class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">Pipeline Screen Tabs (comma-separated)</label>
          <input type="text" id="wiz-screen-stages" value="01-research, 02-spec, 03-review" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
          <span class="text-[10px] text-slate-400 block mt-0.5">Each stage folder forms a tab in the header rail.</span>
        </div>

        <div class="text-xs">
          <label class="block font-semibold text-slate-600 mb-0.5">Layout Pattern</label>
          <select id="wiz-screen-pattern" class="w-full p-1 border rounded focus:outline-none focus:border-accentYellow">
            <option value="2card">2-Card Side-by-Side (Recommended: Data Card + Decision Card)</option>
            <option value="single">Single Card Layout (Standard Centered)</option>
          </select>
          <span class="text-[10px] text-slate-400 block mt-0.5">Side-by-side places information alongside active user prompt buttons.</span>
        </div>

        <button onclick="generateWizardScreens()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 rounded text-xs transition-colors mt-2">Calculate Screen Assets</button>
      </div>

      <!-- Action output instructions -->
      <div class="bg-slate-900 p-3 rounded-lg flex flex-col font-mono text-[10px] shadow-sm justify-between min-h-0">
        <div class="flex-1 flex flex-col min-h-0">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-2 border-b border-slate-800 pb-1 shrink-0">
            <span>Layout Config (_layout.json)</span>
            <button onclick="copyCode('wiz-screen-output')" class="text-emerald-400 font-bold hover:underline">Copy Code</button>
          </div>
          <textarea id="wiz-screen-output" readonly class="flex-1 w-full bg-slate-950 text-slate-200 p-2 border border-slate-850 rounded resize-none outline-none leading-tight font-mono text-[10px] min-h-0"></textarea>
        </div>
        <div class="border-t border-slate-800 pt-2 mt-2 text-[9.5px] text-slate-400 shrink-0 leading-tight">
          <p class="text-emerald-400 font-bold">Steps to configure:</p>
          <ol class="list-decimal pl-3 text-slate-300 mt-1 space-y-0.5">
            <li>Run command: <code class="bg-slate-950 text-accentYellow px-1 py-0.5 rounded font-mono text-[9px]">python3 scripts/setup_screens.py</code></li>
            <li>Input stage names: <code id="wiz-screen-cmd" class="text-accentYellow">01-research, 02-spec, 03-review</code></li>
            <li>Paste this generated coordinate configuration into each stage's <code class="text-slate-200">_layout.json</code> file.</li>
          </ol>
        </div>
      </div>
    </div>
  </div>

  <!-- Tab 5: Cookbook -->
  <div id="content-cookbook" class="flex-1 flex flex-col gap-3 min-h-0 hidden overflow-y-auto pr-1">
    <div class="bg-white p-3 rounded-lg border border-slate-200 flex flex-col gap-3">
      <div>
        <div class="flex justify-between items-center mb-0.5">
          <span class="text-xs font-bold text-slate-700">1. Choice Buttons</span>
          <button onclick="copyCode('code-btn')" class="text-[10px] text-accentYellow font-bold hover:underline">Copy Code</button>
        </div>
        <textarea id="code-btn" readonly class="w-full h-16 p-1.5 bg-slate-900 text-slate-200 font-mono text-[10px] rounded border border-slate-800 resize-none outline-none"><div class="flex gap-2">
  <button onclick="respond('approve')" style="padding: 8px; border-radius: 4px; background: #6f9e6a; color: white;">Approve</button>
  <button onclick="respond('reject')" style="padding: 8px; border-radius: 4px; background: #c2683f; color: white;">Reject</button>
</div></textarea>
      </div>

      <div>
        <div class="flex justify-between items-center mb-0.5">
          <span class="text-xs font-bold text-slate-700">2. Range Slider</span>
          <button onclick="copyCode('code-slider')" class="text-[10px] text-accentYellow font-bold hover:underline">Copy Code</button>
        </div>
        <textarea id="code-slider" readonly class="w-full h-16 p-1.5 bg-slate-900 text-slate-200 font-mono text-[10px] rounded border border-slate-800 resize-none outline-none"><div>
  <input type="range" id="sld" min="0" max="100" value="50" oninput="document.getElementById('lbl').textContent=this.value">
  <span id="lbl">50</span>%
  <button onclick="respond(parseInt(document.getElementById('sld').value))">Submit</button>
</div></textarea>
      </div>

      <div>
        <div class="flex justify-between items-center mb-0.5">
          <span class="text-xs font-bold text-slate-700">3. Radio Buttons</span>
          <button onclick="copyCode('code-radio')" class="text-[10px] text-accentYellow font-bold hover:underline">Copy Code</button>
        </div>
        <textarea id="code-radio" readonly class="w-full h-20 p-1.5 bg-slate-900 text-slate-200 font-mono text-[10px] rounded border border-slate-800 resize-none outline-none"><div style="font-family: sans-serif; font-size: 13px;">
  <label><input type="radio" name="prio" value="low"> Low</label>
  <label><input type="radio" name="prio" value="med" checked> Medium</label>
  <label><input type="radio" name="prio" value="high"> High</label>
  <button onclick="respond(document.querySelector('input[name=\'prio\']:checked').value)">Submit</button>
</div></textarea>
      </div>

      <div>
        <div class="flex justify-between items-center mb-0.5">
          <span class="text-xs font-bold text-slate-700">4. Interactive SVG Bar Chart</span>
          <button onclick="copyCode('code-svg')" class="text-[10px] text-accentYellow font-bold hover:underline">Copy Code</button>
        </div>
        <textarea id="code-svg" readonly class="w-full h-24 p-1.5 bg-slate-900 text-slate-200 font-mono text-[10px] rounded border border-slate-800 resize-none outline-none"><div style="font-family: sans-serif; font-size: 13px;">
  <svg viewBox="0 0 200 100" style="width: 100%; border-bottom: 1px solid #ccc; background: #fafafa;">
    <rect x="25" y="30" width="30" height="60" fill="#e0a23c" rx="2" />
    <text x="40" y="25" font-size="8" text-anchor="middle">75%</text>
    <text x="40" y="98" font-size="7" text-anchor="middle" fill="#666">Accuracy</text>
    <rect x="85" y="10" width="30" height="80" fill="#6f9e6a" rx="2" />
    <text x="100" y="5" font-size="8" text-anchor="middle">95%</text>
    <text x="100" y="98" font-size="7" text-anchor="middle" fill="#666">Speed</text>
  </svg>
  <button onclick="respond('approved')" style="margin-top: 8px;">Approve Metrics</button>
</div></textarea>
      </div>
    </div>
  </div>

  <!-- Tab 6: Guide -->
  <div id="content-guide" class="flex-1 flex flex-col gap-3 min-h-0 hidden overflow-y-auto pr-1">
    <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm text-xs leading-relaxed text-slate-700 space-y-4">
      <div>
        <h3 class="text-sm font-bold text-slate-900 border-b border-slate-100 pb-1 mb-2">🎯 The Baseline: Plain Markdown Cards</h3>
        <p class="mb-2">By default, every card on your board is just a <strong>plain Markdown (.md) file</strong>. This is the fundamental starting point:</p>
        <ul class="list-disc pl-4 space-y-1">
          <li><strong>Tabs</strong>: Every subfolder inside <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">_tv/screens/</code> forms a tab (e.g. <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">demo/</code>).</li>
          <li><strong>Cards</strong>: Every <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">.md</code> file in a screen folder renders as a card.</li>
          <li><strong>Writing</strong>: You can write standard text, headers, tables, and bullet points. No code is required.</li>
        </ul>
      </div>

      <div>
        <h3 class="text-sm font-bold text-slate-900 border-b border-slate-100 pb-1 mb-2">🎛️ Adding HTML (Only When Necessary)</h3>
        <p class="mb-2">You only need to write HTML in two cases:</p>
        <ul class="list-disc pl-4 space-y-1">
          <li><strong>Custom Formatting</strong>: When Markdown is insufficient for custom layout structures.</li>
          <li><strong>Interactive Checkpoints</strong>: When you need simple controls (like buttons, sliders, or forms) to send choice responses back to the agent.
            <ul class="list-circle pl-4 mt-1 space-y-0.5 text-slate-500">
              <li>Set <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">type: interactive</code> and <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">status: blocked</code> in card frontmatter.</li>
              <li>Use simple HTML controls that call <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">respond(value)</code> when clicked.</li>
              <li>This writes to <code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">_tv/responses/<screen>/<id>.md</code> for the agent to read.</li>
            </ul>
          </li>
        </ul>
      </div>

      <div>
        <h3 class="text-sm font-bold text-slate-900 border-b border-slate-100 pb-1 mb-2">🧠 Custom Agent Skills & Wizards</h3>
        <p class="mb-2">CCTV provides both web-based wizards (see the <strong>Card UI Wizard</strong> and <strong>Screen Wizard</strong> tabs above) and optional terminal helper scripts:</p>
        <ul class="list-disc pl-4 space-y-1">
          <li><strong>Card UI & Screen Wizards</strong>: Adjust layouts and build basic HTML controls directly in your browser. Use these if you don't want to run Python scripts or want to understand how it works.</li>
          <li><strong>Interactive Card Builder (<code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">scripts/generate_card.py</code>)</strong>: CLI tool to bootstrap templates.</li>
          <li><strong>Screen Layout Setup (<code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-[10px]">scripts/setup_screens.py</code>)</strong>: CLI tool to setup coordinates.</li>
        </ul>
      </div>

      <div>
        <h3 class="text-sm font-bold text-slate-900 border-b border-slate-100 pb-1 mb-2">🔄 The ICM to CCTV Data Loop</h3>
        <p class="mb-2">An ICM stage outputs a file, and for CCTV, a corresponding card file is written in the relevant screens directory to display it. The next stage reads the previous stage output (which can be edited by the user directly or updated via an interactive response) and creates its own screen card in the same way.</p>
        <div class="space-y-3 bg-slate-50 p-2.5 rounded border border-slate-150 font-mono text-[10px] text-slate-600">
          <div>
            <span class="text-slate-900 font-bold">Case A: AI Writes Card (Stage Output)</span>
            <pre class="bg-white p-1 rounded border mt-1">_tv/screens/01-research/001-findings.md  &lt;-- [Written by AI]</pre>
          </div>
          <div>
            <span class="text-slate-900 font-bold">Case B: User Direct-Edits Card Text</span>
            <pre class="bg-white p-1 rounded border mt-1">_tv/screens/01-research/001-findings.md  &lt;-- [Updated by User in browser]</pre>
          </div>
          <div>
            <span class="text-slate-900 font-bold">Case C: User Interactive Response</span>
            <pre class="bg-white p-1 rounded border mt-1">_tv/responses/02-spec/002-checkpoint.md  &lt;-- [Written by response button]</pre>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Tab 7: Pipeline Simulator (New!) -->
  <div id="content-simulator" class="flex-1 flex flex-col gap-3 min-h-0 hidden">
    <div class="grid grid-cols-1 md:grid-cols-5 gap-3 flex-1 min-h-0 overflow-auto">
      
      <!-- Left Panel: Mock File Tree -->
      <div class="md:col-span-2 bg-slate-900 text-slate-350 p-3 rounded-lg border border-slate-800 shadow-sm flex flex-col min-h-0 overflow-y-auto">
        <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2 shrink-0">
          <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Mock Workspace Files</h2>
          <span class="text-[9px] text-slate-500 font-mono">icm-television/</span>
        </div>
        
        <!-- File Tree -->
        <div class="font-mono text-[11px] leading-relaxed flex-1 space-y-1.5">
          
          <div class="flex items-center gap-1.5 text-slate-400">
            <span>📁</span> <span class="font-semibold text-slate-300">workspace</span>
          </div>
          
          <div class="pl-4">
            <!-- Standard ICM Stages -->
            <div class="flex items-center gap-1.5 text-slate-400">
              <span>📁</span> <span class="text-indigo-300 font-semibold">stages (Standard ICM Folders)</span>
            </div>
            
            <div class="pl-4 border-l border-slate-800 ml-2">
              <div class="flex items-center gap-1.5 text-slate-400">
                <span>📁</span> <span>01-research</span>
              </div>
              
              <div class="pl-4 border-l border-slate-800 ml-2">
                <div class="flex items-center gap-1.5 text-slate-400">
                  <span>📁</span> <span>output</span>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-sources" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">sources.md</span></span>
                    <span id="sim-badge-sources" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
              </div>
            </div>

            <div class="pl-4 border-l border-slate-800 ml-2">
              <div class="flex items-center gap-1.5 text-slate-400">
                <span>📁</span> <span>02-spec</span>
              </div>
              
              <div class="pl-4 border-l border-slate-800 ml-2">
                <div class="flex items-center gap-1.5 text-slate-400">
                  <span>📁</span> <span>output</span>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-spec-src" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">spec.md</span></span>
                    <span id="sim-badge-spec-src" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Optional CCTV Layer -->
            <div class="flex items-center gap-1.5 text-slate-400 mt-3">
              <span>📁</span> <span class="text-amber-400 font-semibold">_tv (Optional Visual CCTV Layer)</span>
            </div>
            
            <div class="pl-4 border-l border-slate-800 ml-2">
              <div class="flex items-center gap-1.5 text-slate-400">
                <span>📁</span> <span>screens</span>
              </div>
              
              <div class="pl-4 border-l border-slate-800 ml-2">
                <div class="flex items-center gap-1.5 text-slate-400">
                  <span>📁</span> <span>01-research</span>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-findings" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">001-findings.md</span></span>
                    <span id="sim-badge-findings" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
              </div>
              
              <div class="pl-4 border-l border-slate-800 ml-2">
                <div class="flex items-center gap-1.5 text-slate-400">
                  <span>📁</span> <span>02-spec</span>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-spec" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">001-spec.md</span></span>
                    <span id="sim-badge-spec" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-checkpoint" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">002-checkpoint.md</span></span>
                    <span id="sim-badge-checkpoint" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="pl-4 border-l border-slate-800 ml-2 mt-2">
              <div class="flex items-center gap-1.5 text-slate-400">
                <span>📁</span> <span>responses</span>
              </div>
              
              <div class="pl-4 border-l border-slate-800 ml-2">
                <div class="flex items-center gap-1.5 text-slate-400">
                  <span>📁</span> <span>02-spec</span>
                </div>
                
                <div class="pl-4 border-l border-slate-800 ml-2">
                  <div id="sim-file-response" class="flex justify-between items-center p-1 rounded border border-transparent transition-all">
                    <span class="flex items-center gap-1.5">📄 <span class="text-slate-300">002-checkpoint.md</span></span>
                    <span id="sim-badge-response" class="text-[9px] px-1 rounded hidden font-semibold"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Panel: Step Controls & Mini CCTV Board -->
      <div class="md:col-span-3 flex flex-col gap-3 min-h-0">
        
        <!-- Step Walkthrough controls -->
        <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-2 shrink-0">
          <div class="flex justify-between items-center">
            <h2 id="sim-step-title" class="text-xs font-bold text-slate-900">Step 1: Stage 1 Begins (AI Writes Output & Mirror Card)</h2>
            <div class="flex gap-1">
              <button onclick="changeSimStep(-1)" id="sim-btn-prev" class="px-2 py-0.5 text-[10px] font-semibold border border-slate-200 rounded hover:bg-slate-50 transition-colors disabled:opacity-50" disabled>&lt; Back</button>
              <button onclick="changeSimStep(1)" id="sim-btn-next" class="px-2 py-0.5 text-[10px] font-semibold bg-accentYellow hover:bg-amber-500 text-slate-900 rounded transition-colors">Next &gt;</button>
            </div>
          </div>
          
          <p id="sim-step-desc" class="text-[11px] leading-relaxed text-slate-600"></p>
          
          <!-- Step Indicators -->
          <div class="flex justify-between text-[9px] font-bold text-slate-400 border-t border-slate-100 pt-2 mt-1 gap-1 overflow-x-auto">
            <button onclick="jumpToSimStep(1)" id="sim-dot-1" class="border-b-2 border-accentYellow text-slate-900 pb-0.5 transition-all whitespace-nowrap">1. Stage 1 Start</button>
            <button onclick="jumpToSimStep(2)" id="sim-dot-2" class="border-b-2 border-transparent hover:text-slate-700 pb-0.5 transition-all whitespace-nowrap">2. User Edit</button>
            <button onclick="jumpToSimStep(3)" id="sim-dot-3" class="border-b-2 border-transparent hover:text-slate-700 pb-0.5 transition-all whitespace-nowrap">3. Stage 2 Start</button>
            <button onclick="jumpToSimStep(4)" id="sim-dot-4" class="border-b-2 border-transparent hover:text-slate-700 pb-0.5 transition-all whitespace-nowrap">4. User Response</button>
          </div>
        </div>
        
        <!-- Mini Board Preview -->
        <div class="flex-1 bg-slate-950 p-2.5 rounded-lg border border-slate-800 flex flex-col min-h-0 shadow-inner">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-2 border-b border-slate-900 pb-1.5 shrink-0">
            <span>Mini CCTV Board Simulation</span>
            <span class="text-indigo-400 font-bold">PREVIEW</span>
          </div>
          
          <!-- Mini Tabs Bar -->
          <div class="flex border-b border-slate-900 text-[10px] font-semibold mb-2 gap-0.5 shrink-0">
            <div id="sim-tab-research" class="px-2 py-1 border-b-2 border-accentYellow text-slate-200">01-research</div>
            <div id="sim-tab-spec" class="px-2 py-1 border-b-2 border-transparent text-slate-500">02-spec</div>
          </div>
          
          <!-- Mini Board Content -->
          <div class="flex-1 flex gap-2 overflow-auto items-start p-1 bg-slate-950 relative min-h-0">
            <div id="sim-cards-container" class="w-full h-full grid grid-cols-1 sm:grid-cols-2 gap-2"></div>
          </div>
        </div>
        
      </div>
      
    </div>
  </div>

  <!-- Script logic -->
  <script>
    // State management
    const state = {
      selection: "None",
      sliderValue: 50,
      priority: "medium"
    };

    function updatePreview() {
      document.getElementById('payload-preview').textContent = JSON.stringify(state, null, 2);
    }

    function updateSelection(val) {
      state.selection = val;
      updatePreview();
    }

    function updateSlider(val) {
      state.sliderValue = parseInt(val);
      document.getElementById('slider-txt').textContent = val + "%";
      updatePreview();
    }

    function updateRadio(val) {
      state.priority = val;
      updatePreview();
    }

    function sendPayload() {
      if (typeof window.respond === 'function') {
        window.respond(state);
      } else {
        alert("The board response bridge is not loaded inside this preview window, but the payload is ready!");
      }
    }

    // Chart updating
    function updateChartBar(bar, val) {
      const rect = document.getElementById('bar-' + bar);
      const text = document.getElementById('lbl-' + bar);
      const num = parseInt(val);
      
      const h = Math.round(num * 0.8);
      const y = 90 - h;
      
      rect.setAttribute('height', h);
      rect.setAttribute('y', y);
      text.setAttribute('y', y - 6);
      text.textContent = num + "%";
    }

    // Tab switching
    function switchTab(tabId) {
      ['playground', 'charts', 'wizard-card', 'wizard-screen', 'cookbook', 'guide', 'simulator'].forEach(t => {
        document.getElementById('content-' + t).classList.add('hidden');
        document.getElementById('tab-' + t).classList.remove('border-accentYellow', 'text-slate-900');
        document.getElementById('tab-' + t).classList.add('border-transparent', 'text-slate-500');
      });
      document.getElementById('content-' + tabId).classList.remove('hidden');
      document.getElementById('tab-' + tabId).classList.add('border-accentYellow', 'text-slate-900');
      document.getElementById('tab-' + tabId).classList.remove('border-transparent', 'text-slate-500');
      
      // Auto generate wizards when switching to make sure output is populated
      if (tabId === 'wizard-card') generateWizardCard();
      if (tabId === 'wizard-screen') generateWizardScreens();
      if (tabId === 'simulator') jumpToSimStep(1);
    }

    // Copy to clipboard helper
    function copyCode(id) {
      const copyText = document.getElementById(id);
      copyText.select();
      copyText.setSelectionRange(0, 99999);
      navigator.clipboard.writeText(copyText.value);
      alert("Code copied to clipboard!");
    }

    // Card Wizard visibility toggle
    function onWizardUIChange(uiVal) {
      document.getElementById('wiz-options-container').classList.add('hidden');
      document.getElementById('wiz-slider-container').classList.add('hidden');
      document.getElementById('wiz-chart-container').classList.add('hidden');
      
      if (uiVal === 'buttons' || uiVal === 'radio' || uiVal === 'checkboxes') {
        document.getElementById('wiz-options-container').classList.remove('hidden');
      } else if (uiVal === 'slider') {
        document.getElementById('wiz-slider-container').classList.remove('hidden');
      } else if (uiVal === 'chart') {
        document.getElementById('wiz-chart-container').classList.remove('hidden');
      }
      generateWizardCard();
    }

    // Generate Card Wizard Code
    function generateWizardCard() {
      const screen = document.getElementById('wiz-card-screen').value.trim();
      const id = document.getElementById('wiz-card-id').value.trim();
      const title = document.getElementById('wiz-card-title').value.trim();
      const prompt = document.getElementById('wiz-card-prompt').value.trim();
      const ui = document.getElementById('wiz-card-ui').value;
      const opts = document.getElementById('wiz-card-options').value.split(',').map(o => o.trim()).filter(Boolean);

      let html = '';
      if (ui === 'buttons') {
        const btnHtml = opts.map(o => {
          const slug = o.toLowerCase().replace(/ /g, '-');
          return `  <button onclick="respond('${slug}')" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; background: white; cursor: pointer;">${o}</button>`;
        }).join('\n');
        html = `<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 8px;">\n  <p>${prompt}</p>\n${btnHtml}\n</div>`;
      } else if (ui === 'slider') {
        const min = document.getElementById('wiz-slider-min').value;
        const max = document.getElementById('wiz-slider-max').value;
        const def = document.getElementById('wiz-slider-def').value;
        html = `<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">\n  <p>${prompt}</p>\n  <div>\n    <label>${prompt} (<span id="lbl">${def}</span>):</label>\n    <input type="range" id="sld" min="${min}" max="${max}" value="${def}" style="width:100%;" oninput="document.getElementById('lbl').textContent=this.value">\n  </div>\n  <button onclick="respond(parseInt(document.getElementById('sld').value))" style="padding:6px; background:#e0a23c; border:none; border-radius:4px; cursor:pointer;">Submit</button>\n</div>`;
      } else if (ui === 'radio') {
        const radHtml = opts.map(o => {
          const slug = o.toLowerCase().replace(/ /g, '-');
          return `  <label style="display:block; margin: 4px 0;"><input type="radio" name="wiz-rad" value="${slug}"> ${o}</label>`;
        }).join('\n');
        html = `<div style="font-family: sans-serif; padding: 10px; font-size: 13px;">\n  <p>${prompt}</p>\n${radHtml}\n  <button onclick="respond(document.querySelector('input[name=\\'wiz-rad\\']:checked').value)" style="margin-top:8px; padding:6px; background:#e0a23c; border:none; border-radius:4px; cursor:pointer;">Submit</button>\n</div>`;
      } else if (ui === 'checkboxes') {
        const cbHtml = opts.map(o => {
          const slug = o.toLowerCase().replace(/ /g, '-');
          return `  <label style="display:block; margin: 4px 0;"><input type="checkbox" value="${slug}"> ${o}</label>`;
        }).join('\n');
        html = `<div style="font-family: sans-serif; padding: 10px; font-size: 13px;">\n  <p>${prompt}</p>\n${cbHtml}\n  <button onclick="submitCheckboxes()" style="margin-top:8px; padding:6px; background:#e0a23c; border:none; border-radius:4px; cursor:pointer;">Submit</button>\n</div>\n<script>\nfunction submitCheckboxes() {\n  const selected = [];\n  document.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => selected.push(cb.value));\n  respond(selected);\n}\n<\/script>`;
      } else if (ui === 'chart') {
        const vals = document.getElementById('wiz-chart-vals').value.split(',').map(v => parseInt(v.trim())).filter(v => !isNaN(v));
        const lbls = document.getElementById('wiz-chart-lbls').value.split(',').map(l => l.trim()).filter(Boolean);
        
        let svgBars = '';
        const width = 30, gap = 20, start_x = 25;
        vals.forEach((v, idx) => {
          const l = lbls[idx] || ('Metric ' + (idx + 1));
          const x = start_x + idx * (width + gap);
          const h = Math.round(v * 0.8);
          const y = 90 - h;
          svgBars += `    <rect x="${x}" y="${y}" width="${width}" height="${h}" fill="#e0a23c" rx="2" />\n`;
          svgBars += `    <text x="${x + width/2}" y="${y - 4}" font-size="8" font-weight="bold" text-anchor="middle">${v}%</text>\n`;
          svgBars += `    <text x="${x + width/2}" y="98" font-size="7" text-anchor="middle" fill="#666">${l}</text>\n`;
        });
        
        html = `<div style="font-family: sans-serif; padding: 10px; font-size: 13px;">\n  <p>${prompt}</p>\n  <svg viewBox="0 0 200 100" style="width:100%; border-bottom:1px solid #ccc; background:#fafafa; margin: 8px 0;">\n${svgBars}  </svg>\n  <button onclick="respond('approve')" style="padding:6px; background:#6f9e6a; border:none; border-radius:4px; color:white; cursor:pointer; width:100%;">Approve metrics</button>\n</div>`;
      }

      const out = `---\nid: ${id}\ntitle: ${title}\ntype: interactive\nstatus: blocked\n---\n${html}`;
      document.getElementById('wiz-card-output').value = out;
      document.getElementById('wiz-card-path').textContent = `_tv/screens/${screen}/${id}.md`;
    }

    // Generate Screen Wizard Setup
    function generateWizardScreens() {
      const stagesStr = document.getElementById('wiz-screen-stages').value;
      const stages = stagesStr.split(',').map(s => s.trim()).filter(Boolean);
      const pattern = document.getElementById('wiz-screen-pattern').value;

      document.getElementById('wiz-screen-cmd').textContent = stages.join(', ');

      let layoutObj = {};
      if (pattern === '2card') {
        layoutObj = {
          "001-welcome": { "x": 24, "y": 24, "w": 340, "h": 260, "z": 0, "pinned": true },
          "002-checkpoint": { "x": 380, "y": 24, "w": 332, "h": 260, "z": 1, "pinned": false }
        };
      } else {
        layoutObj = {
          "001-welcome": { "x": 24, "y": 24, "w": 342, "h": 232, "z": 0, "pinned": false }
        };
      }

      document.getElementById('wiz-screen-output').value = JSON.stringify(layoutObj, null, 2);
    }

    // Pipeline Simulator Logic
    const simData = {
      1: {
        title: "Step 1: Stage 1 Begins (AI Writes Output & Mirror Card)",
        desc: "🤖 <strong>Stage 1 runs:</strong> The AI agent writes its primary findings to the standard ICM stage folder: <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>stages/01-research/output/sources.md</code>.<br/>As an optional visual layer, the agent also writes a card <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>001-findings.md</code> under <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>_tv/screens/01-research/</code> to mirror and display the results on the CCTV board.<br/><br/><span class='text-indigo-400 font-bold'>Case A: AI Stage Outputs a Card</span>",
        activeTab: "01-research",
        files: {
          sources: { border: "border-emerald-500 bg-emerald-950/20", badge: "[CREATED]", badgeClass: "bg-emerald-500 text-white" },
          findings: { border: "border-emerald-500 bg-emerald-950/20", badge: "[CCTV MIRROR]", badgeClass: "bg-emerald-600 text-white" },
          'spec-src': null,
          spec: null,
          checkpoint: null,
          response: null
        },
        cards: [
          {
            id: "001-findings",
            title: "001-findings.md",
            type: "card",
            status: "running",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5'>Stage 1 Research Results</h3><p class='text-[10px] text-slate-400 mb-1'>source: stages/01-research/output/sources.md</p><ul class='list-disc pl-3 text-[10px] space-y-0.5 text-slate-650'><li>Reviewing codebase structure...</li><li>Detected 3 main design patterns.</li><li>Standard plain markdown is the baseline.</li></ul>"
          }
        ]
      },
      2: {
        title: "Step 2: User Direct-Edits Card (Updates Standard ICM File)",
        desc: "✍️ <strong>User modifies findings:</strong> You click the findings card body directly in the browser and edit the text. Because the card links to <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>sources.md</code>, saving the card writes your edits back to the standard ICM stage folder. The next stage will consume this updated text.<br/><br/><span class='text-amber-400 font-bold'>Case B: User Direct-Edits Card Text</span>",
        activeTab: "01-research",
        files: {
          sources: { border: "border-amber-500 bg-amber-950/20", badge: "[USER EDITED]", badgeClass: "bg-amber-500 text-white" },
          findings: { border: "border-amber-500 bg-amber-950/20", badge: "[UPDATED]", badgeClass: "bg-amber-600 text-white" },
          'spec-src': null,
          spec: null,
          checkpoint: null,
          response: null
        },
        cards: [
          {
            id: "001-findings",
            title: "001-findings.md",
            type: "card",
            status: "running",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5 text-amber-700'>Stage 1 Research Results (Edited)</h3><p class='text-[10px] text-slate-400 mb-1'>source: stages/01-research/output/sources.md</p><ul class='list-disc pl-3 text-[10px] space-y-0.5 text-slate-650'><li>Reviewing codebase structure...</li><li>Detected 3 main design patterns.</li><li class='bg-amber-50 text-amber-950 px-1 rounded font-semibold'>[USER EDIT] Focus on Case A/B/C trees</li></ul>"
          }
        ]
      },
      3: {
        title: "Step 3: Stage 2 Starts (AI Writes Checkpoint)",
        desc: "🤖 <strong>Stage 2 (Spec Design) runs:</strong> The agent reads the findings from <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>sources.md</code> (with your user edit), writes a spec mirror draft card and an interactive checkpoint card <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>002-checkpoint.md</code>. The agent's execution blocks, waiting for human action.<br/><br/><span class='text-emerald-400 font-bold'>Case A: AI Writes Card & Checkpoint</span>",
        activeTab: "02-spec",
        files: {
          sources: null,
          findings: null,
          'spec-src': null,
          spec: { border: "border-emerald-500 bg-emerald-950/20", badge: "[CCTV MIRROR]", badgeClass: "bg-emerald-500 text-white" },
          checkpoint: { border: "border-rose-500 bg-rose-950/20", badge: "[BLOCKED]", badgeClass: "bg-rose-500 text-white" },
          response: null
        },
        cards: [
          {
            id: "001-spec",
            title: "001-spec.md",
            type: "card",
            status: "running",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5'>001-spec.md (Draft Spec)</h3><p class='text-[10px] text-slate-650'>Spec details alignment coordinates of the cards on the board.</p>"
          },
          {
            id: "002-checkpoint",
            title: "002-checkpoint.md",
            type: "interactive",
            status: "blocked",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5 text-rose-700'>Checkpoint: Spec Layout</h3><p class='text-[10px] text-slate-650 mb-2'>Do you approve the proposed spec coordinates?</p><div class='flex gap-1.5'><button onclick='simulateApproval()' class='flex-1 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[10px] font-bold transition-all'>Approve</button><button class='flex-1 py-1 border border-slate-300 text-slate-700 hover:bg-slate-50 rounded text-[10px] transition-all'>Revision</button></div>"
          }
        ]
      },
      4: {
        title: "Step 4: User Actions Checkpoint (Writes Response & Completes)",
        desc: "👆 <strong>User clicks 'Approve':</strong> Clicking the button writes the response to <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>_tv/responses/02-spec/002-checkpoint.md</code>. Stage 2 resumes, consumes the response, and writes the standard ICM spec file: <code class='bg-slate-800 text-slate-200 px-1 py-0.5 rounded font-mono text-[10px]'>stages/02-spec/output/spec.md</code>. The checkpoint card updates to done.<br/><br/><span class='text-indigo-400 font-bold'>Case C: User Interactive Response</span>",
        activeTab: "02-spec",
        files: {
          sources: null,
          findings: null,
          'spec-src': { border: "border-emerald-500 bg-emerald-950/20", badge: "[CREATED]", badgeClass: "bg-emerald-500 text-white" },
          spec: { border: "border-emerald-500 bg-emerald-950/20", badge: "[CCTV MIRROR]", badgeClass: "bg-emerald-600 text-white" },
          checkpoint: null,
          response: { border: "border-indigo-500 bg-indigo-950/20", badge: "[RESPONSE WRITTEN]", badgeClass: "bg-indigo-500 text-white" }
        },
        cards: [
          {
            id: "001-spec",
            title: "001-spec.md",
            type: "card",
            status: "running",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5'>001-spec.md (Draft Spec)</h3><p class='text-[10px] text-slate-650'>Spec details alignment coordinates of the cards on the board.</p>"
          },
          {
            id: "002-checkpoint",
            title: "002-checkpoint.md",
            type: "interactive",
            status: "done",
            body: "<h3 class='font-bold text-xs text-slate-800 mb-1 border-b pb-0.5 text-emerald-700'>Checkpoint: Spec Layout</h3><p class='text-[10px] text-slate-650 mb-2'>Do you approve the proposed spec coordinates?</p><div class='bg-emerald-50 border border-emerald-200 text-emerald-950 p-1.5 rounded text-center text-[10px] font-bold'>Approved! Response written to file.</div>"
          }
        ]
      }
    };

    let currentSimStep = 1;

    function renderSimStep(step) {
      currentSimStep = step;
      const data = simData[step];
      
      document.getElementById('sim-step-title').innerHTML = data.title;
      document.getElementById('sim-step-desc').innerHTML = data.desc;
      
      document.getElementById('sim-btn-prev').disabled = (step === 1);
      document.getElementById('sim-btn-next').disabled = (step === 4);
      
      for (let i = 1; i <= 4; i++) {
        const dot = document.getElementById('sim-dot-' + i);
        if (i === step) {
          dot.className = "border-b-2 border-indigo-650 text-indigo-400 pb-0.5 font-bold transition-all text-[10px] whitespace-nowrap";
        } else {
          dot.className = "border-b-2 border-transparent text-slate-400 hover:text-slate-700 pb-0.5 transition-all text-[10px] whitespace-nowrap";
        }
      }
      
      const tabResearch = document.getElementById('sim-tab-research');
      const tabSpec = document.getElementById('sim-tab-spec');
      if (data.activeTab === '01-research') {
        tabResearch.className = "px-2 py-1 border-b-2 border-accentYellow text-slate-200";
        tabSpec.className = "px-2 py-1 border-b-2 border-transparent text-slate-500";
      } else {
        tabResearch.className = "px-2 py-1 border-b-2 border-transparent text-slate-500";
        tabSpec.className = "px-2 py-1 border-b-2 border-accentYellow text-slate-200";
      }
      
      const files = ['sources', 'spec-src', 'findings', 'spec', 'checkpoint', 'response'];
      files.forEach(f => {
        const fileNode = document.getElementById('sim-file-' + f);
        const fileBadge = document.getElementById('sim-badge-' + f);
        const fData = data.files[f];
        
        if (fData) {
          fileNode.className = `flex justify-between items-center p-1 rounded border transition-all ${fData.border}`;
          fileBadge.className = `text-[9px] px-1 rounded font-semibold ${fData.badgeClass}`;
          fileBadge.textContent = fData.badge;
          fileBadge.classList.remove('hidden');
        } else {
          fileNode.className = "flex justify-between items-center p-1 rounded border border-transparent transition-all";
          fileBadge.className = "text-[9px] px-1 rounded font-semibold hidden";
          fileBadge.textContent = "";
        }
      });
      
      const container = document.getElementById('sim-cards-container');
      container.innerHTML = '';
      
      data.cards.forEach(c => {
        const cardDiv = document.createElement('div');
        cardDiv.className = "bg-white border border-slate-200 rounded p-2 flex flex-col justify-between shadow-sm relative h-36 overflow-y-auto";
        
        let statusBadge = '';
        if (c.status === 'blocked') {
          statusBadge = '<span class="px-1 py-0.5 rounded bg-rose-100 text-rose-800 text-[8px] font-bold uppercase">Blocked</span>';
        } else if (c.status === 'done') {
          statusBadge = '<span class="px-1 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[8px] font-bold uppercase">Done</span>';
        } else {
          statusBadge = '<span class="px-1 py-0.5 rounded bg-slate-105 text-slate-600 text-[8px] font-bold uppercase">Running</span>';
        }
        
        cardDiv.innerHTML = `
          <div class="flex justify-between items-center border-b border-slate-100 pb-1 mb-1.5 shrink-0">
            <span class="text-[9px] font-bold text-slate-500 font-mono">${c.title}</span>
            ${statusBadge}
          </div>
          <div class="flex-1 font-sans text-xs">
            ${c.body}
          </div>
        `;
        container.appendChild(cardDiv);
      });
    }
    
    function changeSimStep(dir) {
      const nextStep = currentSimStep + dir;
      if (nextStep >= 1 && nextStep <= 4) {
        renderSimStep(nextStep);
      }
    }
    
    function jumpToSimStep(step) {
      renderSimStep(step);
    }

    function simulateApproval() {
      jumpToSimStep(4);
    }
  </script>
</body>
</html>
