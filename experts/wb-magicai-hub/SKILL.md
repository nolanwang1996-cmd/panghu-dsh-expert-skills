---
name: wb-magicai-hub
description: 多 AI 能力的编排与集成：模型选择、prompt 管理、能力组合与成本控制。
---
# AI 能力编排专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 模块：gdscript-codegen

# GDScript 代码生成 Skill

> **用途**：AI 生成高质量 GDScript 代码的规范和模板  
> **版本**：v1.0 · 2026-04-22  
> **适用引擎**：Godot 4.5/4.6

---

## 一、GDScript 4.x 核心规范

### 1.1 类型系统

Godot 4.x 使用强类型 GDScript，AI 生成代码时必须遵循：

```gdscript
# ✅ 推荐：显式类型标注
var health: int = 100
var speed: float = 10.0
var player_name: String = "Player"
var position: Vector3 = Vector3.ZERO
var enemies: Array[Node3D] = []
var weapon_data: Dictionary = {}

# ✅ 推荐：函数参数和返回值标注
func take_damage(amount: int) -> void:
    health -= amount

func get_health_ratio() -> float:
    return float(health) / float(max_health)

# ❌ 避免：无类型标注（编译器警告）
var health = 100  # 类型推断，但不推荐
```

### 1.2 类型推断陷阱

```gdscript
# ❌ 错误：for 循环迭代变量无法推断
for x in [-1.0, 1.0]:
    var pos := center + Vector2(x, 0) * radius  # 报错！

# ✅ 正确：显式标注迭代变量
for x: float in [-1.0, 1.0]:
    var pos := center + Vector2(x, 0) * radius

# ❌ 错误：字典值类型无法推断
var data = {"a": 1, "b": 2}
var value := data["a"]  # 报错！

# ✅ 正确：显式标注或使用 as
var value: int = data["a"]
var value := data["a"] as int
```

### 1.3 信号声明

```gdscript
# Godot 4.x 信号语法
signal health_changed(current: int, maximum: int)
signal died
signal damage_taken(amount: int, remaining: int)
signal weapon_changed(weapon_index: int)
```

### 1.4 导出变量

```gdscript
# 基础类型
@export var health: int = 100
@export var speed: float = 10.0

# 范围限制
@export_range(0, 100, 1) var health: int = 100
@export_range(0.0, 10.0, 0.1) var speed: float = 5.0

# 枚举
@export_enum("Easy", "Normal", "Hard") var difficulty: int = 1

# 资源
@export var weapon_resource: WeaponResource
@export var projectile_scene: PackedScene

# 分组
@export_group("Combat")
@export var damage: int = 10
@export var fire_rate: float = 0.5
```

### 1.5 @onready 和节点引用

```gdscript
# ✅ 推荐：@onready 延迟初始化
@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var health_bar: ProgressBar = $UI/HealthBar

# ✅ 推荐：运行时获取（更灵活）
var player: Node3D
func _ready() -> void:
    player = get_tree().get_first_node_in_group("player")

# ❌ 避免：硬编码路径（易断裂）
var health_label = $"../UI/GameHUD/HealthPanel/HealthLabel"
```

---

## 二、常用代码模板

### 2.1 组件脚本模板

```gdscript
# health_component.gd
extends Node
class_name HealthComponent

## 生命值组件 - 可挂载到任何需要 HP 的实体

signal health_changed(current: int, maximum: int)
signal died
signal damage_taken(amount: int, remaining: int)

@export var max_health: int = 100
@export var invincible: bool = false
@export var invincible_time: float = 0.0

var current_health: int
var is_dead: bool = false
var _invincible_timer: float = 0.0

func _ready() -> void:
    current_health = max_health

func take_damage(amount: int) -> void:
    if is_dead or invincible:
        return
    if _invincible_timer > 0:
        return
    
    current_health = max(0, current_health - amount)
    damage_taken.emit(amount, current_health)
    health_changed.emit(current_health, max_health)
    
    if current_health <= 0:
        is_dead = true
        died.emit()

func heal(amount: int) -> void:
    if is_dead:
        return
    current_health = min(max_health, current_health + amount)
    health_changed.emit(current_health, max_health)
```

### 2.2 Manager 脚本模板

```gdscript
# arena_manager.gd
extends Node
class_name ArenaManager

## 竞技场管理器 - 处理限时刷分模式的核心逻辑

signal arena_started
signal arena_ended(final_score: int, rating: String)
signal score_changed(score: int, combo: int)
signal time_changed(remaining: float)

@export var match_duration: float = 60.0
@export var combo_window: float = 3.0

var _score: int = 0
var _combo: int = 0
var _time_remaining: float = 0.0
var _is_active: bool = false

func _ready() -> void:
    set_process(false)

func start_arena() -> void:
    _score = 0
    _combo = 0
    _time_remaining = match_duration
    _is_active = true
    set_process(true)
    arena_started.emit()
```

---

## 三、信号连接规范

```gdscript
# 方法引用（推荐）
button.pressed.connect(_on_button_pressed)

# Lambda（简单逻辑）
timer.timeout.connect(func(): print("Timeout!"))

# 带参数绑定
enemy.died.connect(_on_enemy_died.bind(spawn_point, enemy))

# 一次性连接
button.pressed.connect(_on_one_time_press, CONNECT_ONE_SHOT)
```

---

## 四、代码生成检查清单

AI 生成 GDScript 代码后，检查以下项目：

### 语法检查
- [ ] 所有变量有类型标注
- [ ] for 循环迭代变量有类型标注
- [ ] 函数参数和返回值有类型标注
- [ ] 信号声明格式正确
- [ ] 缩进使用 Tab（不是空格）

### 最佳实践检查
- [ ] 避免硬编码节点路径
- [ ] 使用 @onready 或 _ready() 获取节点
- [ ] 信号连接有错误处理
- [ ] 资源加载有空值检查

### 命名规范检查
- [ ] 类名 PascalCase
- [ ] 变量名 snake_case
- [ ] 私有变量 _snake_case
- [ ] 常量 UPPER_SNAKE_CASE
- [ ] 信号名 snake_case

---

## 五、编辑器警告规避（真实踩过的坑，避免打扰用户）

这一节列的都是 Godot 4 **编辑器错误面板里最常见**、并且**生成式 AI 最容易犯**的警告。每条都给出修复模式，生成代码时直接避开。

### 5.1 变量名与 built-in function 重名

```gdscript
# ❌ 警告：The variable "hash" has the same name as a built-in function.
var hash := _hash_cell(x, z)

# ✅ 改名避开
var cell_hash := _hash_cell(x, z)
# 或在辅助函数内部用 1 字母短名
var h := _hash_u32(seed)
```

**触发名单**（非完全列表）：`hash`、`len`、`str`、`int`、`float`、`bool`、
`print`、`abs`、`sin`、`cos`、`min`、`max`、`clamp`、`lerp`、`sign`、
`type_of`、`range`、`load`、`preload`。生成代码前，**避免用 GDScript
全局函数名做局部变量名**。

### 5.2 局部变量 shadow 基类属性

```gdscript
# ❌ 警告：The local variable "basis" is shadowing an already-declared
#          property in the base class "Node3D".
var basis := Basis(Vector3.UP, yaw)

# ✅ 改名
var cell_basis := Basis(Vector3.UP, yaw)
```

**`Node3D` 高风险属性**：`transform`、`basis`、`position`、`rotation`、
`scale`、`global_transform`、`global_position`、`global_basis`。
**`CanvasItem` 高风险**：`visible`、`modulate`、`material`。
**`Node` 高风险**：`name`、`owner`、`tree`。

生成挂在 Node 继承树上的脚本时，**不要用这些名字做局部变量**。

### 5.3 函数参数未使用

```gdscript
# ❌ 警告：The parameter "threshold" is never used in the function ...
func compute(value: float, threshold: float) -> float:
    return value * 2.0

# ✅ 接口必须保留该参数（callback / signal / polymorphism）时加下划线
func compute(value: float, _threshold: float) -> float:
    return value * 2.0

# ✅ 如果不需要保留签名，直接删掉参数
func compute(value: float) -> float:
    return value * 2.0
```

**判断原则**：
- 参数是为了匹配 signal 签名 / callback 接口 / 多态重载 → 加 `_` 前缀
- 参数确实是历史残留、没人调用指定它 → 删掉

### 5.4 整数除法警告

```gdscript
# ❌ 警告：Integer division. Decimal part will be discarded.
var x_groups := int((size.x - 1) / 8) + 1

# ✅ 选项 A：如果这就是故意的（如 GPU dispatch 组数、tile index 计算）
@warning_ignore("integer_division")
var x_groups := int((size.x - 1) / 8) + 1

# ✅ 选项 B：如果其实想要浮点结果
var x_groups_f := (size.x - 1) / 8.0

# ✅ 选项 C：显式用 @GlobalScope 的 int div 语义更清晰
var x_groups := ((size.x - 1) / 8) + 1  # 全 int 操作数，结果也是 int
```

**判断原则**：除数 / 被除数任一方是 float **则永远不报** ——
`1.0 / 3.0` 安全；`1 / 3` 报警告。

### 5.5 赋值未使用

```gdscript
# ❌ 警告：The value of "result" is never used.
var result := compute()
return

# ✅ 不关心返回值就别赋
compute()
return
```

### 5.6 未使用的 signal

```gdscript
# ❌ 警告：The signal "health_changed" is declared but never used.
signal health_changed(hp: int)

# 生成时：只声明你真正会 emit 的 signal。若是占位留给将来，加注释 +
# @warning_ignore
@warning_ignore("unused_signal")
signal health_changed(hp: int)  # TODO(v2): emit after HP system lands
```

### 5.7 `@warning_ignore` 使用守则

只在**三种情况**使用，别当万灵药：

1. **故意如此**（整数除法 / shadow 是有意的 API 对齐）
2. **接口约束**（签名必须保留某个参数）
3. **待办占位**（signal/field 下个版本才接）

**禁止**：用 `@warning_ignore` 来"压住一个自己没搞清楚的警告"。警告是
Godot 在告诉你某处有 bug 风险 —— 先理解，再决定豁免。

### 5.8 生成前自检清单

AI 在输出 GDScript 前**务必**过一遍：

- [ ] 没有 `var hash / var len / var str / var range / var load / var print` 等重名
- [ ] 如果 `extends Node3D` → 没有 `var basis / var transform / var position / var rotation / var scale`
- [ ] 如果 `extends CanvasItem` / `Control` → 没有 `var visible / var modulate / var material`
- [ ] 函数参数全部有用；接口参数加 `_` 前缀
- [ ] `int / int` 表达式：显式 `@warning_ignore("integer_division")` 或改成 `float`
- [ ] signal 全部会 `emit()`，或显式标记占位
- [ ] 没有"写着玩"的 `var result = foo()` 却不用 result

## 模块：godot-asset-path-surgery

# Godot Asset Path Surgery

> **When to invoke**: user is staring at red errors of the form
> `Cannot open file 'res://old/path/thing.material'` *while the file
> obviously exists at a new path*. This is almost always because a binary
> resource has the old path hard-coded in its payload (Godot bakes
> `ExtResource` paths into `.mesh` / `.material` / `.scn` / compressed
> `.tres` / `.res` at save time).

---

## Core insight

Godot resources carry **two kinds of path information**:

| Kind | Where | Update mechanism |
|---|---|---|
| **Discovery path** (how the editor finds the file) | `.godot/uid_cache.bin`, `<file>.uid` sidecar | Auto-updated by Godot when it sees the file move |
| **Internal ExtResource paths** (who this file references) | **Inside the binary payload** of the file | **Not auto-updated** — the file must be `load()` + `save()` again to rewrite them |

Phase-3-style folder migrations fix kind #1 for free but **silently break kind #2**. Symptom: editor reports broken refs; game often still runs because `load()` can still find the target via UID, but the error panel is polluted and hides real issues.

---

## Decision tree

```
Editor shows: "Cannot open file 'res://<old-path>'"
│
├─ Does the target file exist at the new path?
│  ├─ No  → you actually deleted it. Restore it or fix the reference.
│  └─ Yes → go to next check
│
├─ Is the error coming from a *binary* resource (.mesh/.material/.scn/.res)?
│  ├─ No  → it's a plain .tscn/.tres referencing the old path by text;
│  │       use sed/IDE search-replace on the text file and you're done.
│  └─ Yes → use the surgery pattern below (file's internal payload
│           carries the stale path as UTF-8 bytes).
│
├─ Does the affected binary ALSO depend on another resource that also moved?
│  ├─ No  → Pattern A (simple resave).
│  └─ Yes → Pattern B (shim + reassign + resave), because ResourceLoader
│           refuses to open a file whose ExtResource target is missing.
```

---

## Pattern A — Simple resave (self-contained binary)

**When**: a `.mesh` / `.material` / `.scn` carries a stale *self-path* header
or a stale external path, but the target of that external path still exists
(just at a new location accessible by UID).

```gdscript
# tools/resave_<thing>.gd  -- SceneTree-mode one-shot
extends SceneTree

const PATHS := [
    "res://art/models/<new>/thing.mesh",
    "res://art/models/<new>/thing.material",
]

func _initialize() -> void:
    var failed := 0
    for p in PATHS:
        var res := ResourceLoader.load(p, "", ResourceLoader.CACHE_MODE_IGNORE)
        if res == null:
            push_error("[resave] load failed: %s" % p)
            failed += 1
            continue
        # Force the in-memory resource_path to match the on-disk path so
        # ResourceSaver doesn't keep the stale path baked into the header.
        res.resource_path = p
        # FLAG_COMPRESS preserves the original RSCC compression; without it
        # binary resources (esp. .material) may bloat 3-5x.
        var err := ResourceSaver.save(res, p, ResourceSaver.FLAG_COMPRESS)
        if err != OK:
            push_error("[resave] save failed (%d): %s" % [err, p])
            failed += 1
            continue
        print("[resave] ok: ", p)
    quit(0 if failed == 0 else 1)
```

Run:
```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --quit \
    --path . --script tools/resave_<thing>.gd
```

---

## Pattern B — Shim + reassign (binary with broken ExtResource)

**When**: the binary resource internally references an `ExtResource` whose
*path* is stale, and Godot refuses to open the binary ("Can't load
dependency"). Pattern A won't work because `ResourceLoader.load()` fails
before you can rewrite the resource.

**Strategy**: temporarily place the dependency's current content at the
*old* path so the loader resolves, retarget the reference to the *new*
path in memory, save, clean up the shim.

```gdscript
# tools/resave_<thing>.gd  -- SceneTree-mode one-shot
extends SceneTree

const DEP_NEW := "res://art/models/<new>/material.material"
const DEP_OLD := "res://old/path/material.material"
const DEP_OLD_DIR := "res://old/path"

const BINARY := "res://art/models/<new>/mesh_with_dep.mesh"

func _initialize() -> void:
    # 1. Pre-load the dep from its real path (the one we want baked in).
    var dep := ResourceLoader.load(DEP_NEW, "", ResourceLoader.CACHE_MODE_REUSE)
    if dep == null:
        push_error("cannot load dep at %s" % DEP_NEW)
        quit(1)
        return

    # 2. Shim: copy dep to the old path so the binary's stale ExtResource resolves.
    var da := DirAccess.open("res://")
    var old_dir_rel := DEP_OLD_DIR.replace("res://", "")
    if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(DEP_OLD_DIR)):
        da.make_dir_recursive(old_dir_rel)
    if da.copy(DEP_NEW, DEP_OLD) != OK:
        push_error("temp copy failed")
        quit(1)
        return

    # 3. Now the binary loads. Retarget its material(s) to the canonical
    #    instance whose resource_path is DEP_NEW, not the shim.
    var mesh := ResourceLoader.load(BINARY, "", ResourceLoader.CACHE_MODE_IGNORE) as ArrayMesh
    if mesh != null:
        for i in mesh.get_surface_count():
            mesh.surface_set_material(i, dep)
        mesh.resource_path = BINARY
        ResourceSaver.save(mesh, BINARY, ResourceSaver.FLAG_COMPRESS)
        print("[resave] ok: ", BINARY)

    # 4. Teardown: remove the shim + any dir tree we created.
    da.remove(DEP_OLD)
    _remove_empty_parents_up_to_res(DEP_OLD_DIR)
    quit(0)


func _remove_empty_parents_up_to_res(path: String) -> void:
    var da := DirAccess.open("res://")
    var cur := path
    while cur != "res://" and cur.begins_with("res://"):
        var d := DirAccess.open(cur)
        if d == null: break
        d.list_dir_begin()
        var has_child := false
        while true:
            var n := d.get_next()
            if n == "": break
            if n == "." or n == "..": continue
            has_child = true; break
        d.list_dir_end()
        if has_child: break
        if da.remove(cur) != OK: break
        cur = cur.get_base_dir()
```

Adapt the `surface_set_material()` line to whatever API the binary uses
(e.g. for a PackedScene you'd iterate nodes; for a ShaderMaterial you'd
reassign `shader` or texture params).

---

## Post-surgery verification checklist

Run all three:

1. **No more stale paths in binaries**:
   ```bash
   grep -rln '<old-path-fragment>' . --exclude-dir='.godot'
   ```
   Expected: only your maintenance script (which records the constant).

2. **Headless load smoke test** — drop this into `tools/_smoke.gd` and
   delete after:
   ```gdscript
   extends SceneTree
   func _initialize() -> void:
       var ps := load("res://scenes/.../affected_scene.tscn") as PackedScene
       if ps == null: push_error("FAIL"); quit(1); return
       var inst := ps.instantiate()
       print("OK children=", inst.get_child_count())
       inst.queue_free()
       quit(0)
   ```
   Run:
   ```bash
   /Applications/Godot.app/Contents/MacOS/Godot --headless \
       --path . --script tools/_smoke.gd 2>&1 | grep -E 'ERROR|OK:'
   ```
   Expected: no `ERROR` lines referencing old paths, one `OK children=N`.

3. **Editor visual check** — reopen the editor and watch the error panel.
   For best results: first clear stale caches (see the
   `godot-headless-verify` skill for the safe clean-cache recipe).

---

## Critical gotchas

### Length mismatch kills naive binary sed

```python
# DO NOT DO THIS — it corrupts the file
content = open(f, 'rb').read()
content = content.replace(b'level/textures/Material.material',
                          b'art/models/material.material')  # NEW is longer
open(f, 'wb').write(content)
```

Godot binary resources encode strings as length-prefixed (Pascal-style).
If new path length ≠ old path length, the length prefix still says "51
chars" but the string is now 55 chars — subsequent fields shift, parser
explodes. **Always go through `ResourceLoader`/`ResourceSaver`**, never
touch raw bytes.

### Forgetting `FLAG_COMPRESS`

Default `ResourceSaver.save(res, path)` writes **uncompressed** (`RSRC`
magic). If the original was `RSCC` (compressed), you'll see 3-5x file
bloat. Always pass `ResourceSaver.FLAG_COMPRESS` unless you have a
reason not to.

### `CACHE_MODE_REUSE` vs `CACHE_MODE_IGNORE`

- **IGNORE**: Force a fresh load from disk. Use for the resource you're
  about to mutate and save, so you don't accidentally mutate the editor's
  cached instance.
- **REUSE**: Share with the editor cache. Use for *dependencies* that
  you want other references to keep pointing at.

### `.uid` sidecar

Any new `.gd` file you drop in (like your one-shot `resave_*.gd`) needs a
`.uid` sidecar or the project-specific pre-commit hook will reject the
commit. Generate by running Godot once: `Godot --headless --import --path .`.

---

## Anti-patterns — don't do these

- ❌ **Binary sed**: length mismatch corrupts files (see above).
- ❌ **Duplicate assets at old + new paths**: tempting, but creates two
  copies that diverge. Violates `docs/ASSET_GUIDELINES.md §7`.
- ❌ **Leaving the surgery script in place without telling anyone**:
  mark it clearly as one-shot maintenance, add a header comment
  explaining what bug it fixed (with commit SHA if possible), keep it
  under `tools/` so `check_asset_structure.gd` accepts it.
- ❌ **Running the script without `--headless` first**: user may have the
  editor open, which will race-save stale state back over your fix.

---

## When to NOT use this skill

- **.tscn / .tres text resources**: they're text, do a plain sed or IDE
  global-replace.
- **User can just open-save in editor by hand**: if you're only dealing
  with 1-2 files and the user is comfortable in the editor, point them
  at "FileSystem dock → right-click → Reimport / Save". This skill is
  for 5+ files or when the user wants a reproducible, scripted fix.
- **UID-based references**: Godot 4 uses `uid://...` identifiers that are
  location-independent. If a `.tscn` references `uid://xyz` and the file
  has moved, Godot resolves it via UID cache — no surgery needed, just
  ensure `.godot/uid_cache.bin` is fresh (see `godot-headless-verify`).

---

## Reference: real fix done on TPS demo

Commit `7b94c7b` ("fix(art): rewrite core/*.mesh + Material_001.material
to drop stale Phase 3.6 paths"): after moving `level/textures/structure/Core/`
to `art/models/environment/arena/core/`, 5 binaries still baked the old
path. Script: [`tools/resave_core_meshes.gd`](../../../tools/resave_core_meshes.gd).
Result: 0 editor ERRORs + meshes shrunk 58% thanks to Godot 4.6's newer
compressor.

## 模块：godot-data-driven-config

# Godot Data-Driven Config Skill

## What this skill does

Turns hardcoded `const` / magic numbers inside `.gd` files into a clean **Resource-based config layer** that designers can edit via `.tres` or the Godot Inspector. Also generates a CLI validator (`bash tools/validate_data.sh`) so a human or CI can check "did I break the config table?" in one command.

## When to invoke

Trigger on intents like:
- "Create a WeaponData / EnemyData / LevelData / SkillData for this project"
- "Move these hardcoded numbers into a config table"
- "I want designers to tune damage/hp/speed without touching code"
- "Add a new weapon/enemy type through data"
- "Build an AI-native Godot config workflow"

## Canonical file layout (ALWAYS use this)

```
res://data/
├── specs/                       # JSON specs, source of truth (git-tracked)
│   ├── weapon.spec.json
│   └── ...
├── resources/
│   ├── <name>_data.gd           # class_name <Name>Data extends Resource
│   └── data_manager.gd          # Autoload (AUTOGENERATED — do not hand-edit AUTOGEN regions)
├── <name>s/                     # plural dir, one .tres per entry
│   └── default_<name>.tres
tools/
├── validate_data.gd             # Godot-side CLI validator (autogen)
└── validate_data.sh             # bash wrapper (exit code fix-up)
project.godot                    # [autoload] DataManager="*res://data/resources/data_manager.gd"
```

Rationale: plural-dir + `id` field makes `DirAccess` scanning trivial. Specs under `data/specs/*.spec.json` are the **source of truth**; regenerating `data_manager.gd` / `validate_data.gd` is always a pure function of that directory, so nothing can drift.

## Required workflow

### Step 1 — Discover & propose

1. Read target `.gd` files; collect hardcoded constants and literals.
2. Ask the user which category (weapon/player/enemy/level/skill/item/…). Each category becomes one `<Name>Data` class.
3. Produce a **field mapping table** (source constant → new field → range). Present it, wait for OK (max 1 round of confirmation).

### Step 2 — Write spec JSON under `data/specs/`

Every category is described by exactly one JSON file matching `schemas/field_spec.schema.json`. Commit these to git — they are the source of truth and diff well.

Minimal valid spec:
```json
{
  "name": "weapon",
  "default_id": "default_pistol",
  "fields": [
    { "key": "id", "type": "StringName", "default": "&\"\"", "group": "Identity" },
    { "key": "damage", "type": "int", "default": 10, "range": [0, 9999, 1] }
  ],
  "validators": ["damage >= 0"]
}
```

### Step 3 — Run `scaffold.py` once per new/updated category

```bash
python3 ~/.codebuddy/skills/godot-data-driven-config/scripts/scaffold.py \
    --project-root <abs Godot project path> \
    --spec <abs path to spec>.spec.json
```

The script:
- copies the spec into `res://data/specs/` (creates source-of-truth file)
- writes `res://data/resources/<name>_data.gd` (first time only; re-run with `--force-class` to overwrite)
- writes `res://data/<name>s/default_<name>.tres` (first time only; `--force-tres` to overwrite)
- **rebuilds** `res://data/resources/data_manager.gd` from **all** `data/specs/*.spec.json` — you never lose a previously-added category
- **rebuilds** `res://tools/validate_data.gd` (duck-typed against `Resource`, so cold-start without `.godot/` cache still works)
- writes `res://tools/validate_data.sh` wrapper
- patches `[autoload]` in `project.godot` idempotently

### Step 4 — Migrate consumer `.gd` files

For each file with hardcoded values:
1. Add at top of class:
   ```gdscript
   @export var <name>_data: <Name>Data
   ```
2. In `_ready()`:
   ```gdscript
   if <name>_data == null:
       <name>_data = DataManager.get_<name>()
   ```
3. Replace literal(s): `JUMP_SPEED` → `<name>_data.jump_speed` etc.
4. **Keep purely-technical consts** unchanged (collision masks, shader paths, blend-tree parameter strings).
5. **DO NOT** edit `.tscn` unless necessary — the `DataManager` fallback covers unbound cases.

### Step 5 — Validate

```bash
bash tools/validate_data.sh
# exit 0 = OK
# exit 1 = validation failed (stdout/stderr has reasons)
# exit 2 = environment issue
```

On **cold clone** (no `.godot/` dir), the wrapper auto-refreshes the class cache once via `godot --headless --editor --quit` — designers/CI need no special knowledge.

### Step 6 — Document

Append to `PROJECT_OVERVIEW.md` or `README.md`:
- The mapping table from Step 1
- Designer workflow: "edit `.tres` → run `bash tools/validate_data.sh` → F5".
- Validator command.

## Hard rules

- **One Resource class per category**, never a god-class.
- Numeric fields MUST have `@export_range`.
- Every `<Name>Data` MUST have an `id: StringName` field; filename stem is used as fallback id.
- `DataManager` is ALWAYS an Autoload named `DataManager`.
- `data_manager.gd` returns `Resource` (not `<Name>Data`) from getters; callers cast with `as WeaponData` if they want static typing. This keeps cold-start safe.
- DO NOT mutate a Resource at runtime (shared reference). To modify: `var copy = data.duplicate(); copy.x = ...`.
- DO NOT try to `MultiplayerSynchronizer`-sync a Resource. Instead, guarantee the same `.tres` exists on all peers (git-managed).
- Validator never uses `exit_code` because Godot bug #88055 drops it under `--script`. Use the `VALIDATION_RESULT=OK|FAIL:n` stdout marker (the generated `validate_data.sh` does this).
- DO NOT hand-edit the `# region *_AUTOGEN` blocks; `scaffold.py` rewrites them on every run.

## Cold-start / CI notes

- Godot's `global_script_class_cache.cfg` is created by the editor. For headless/CI, the first run needs `godot --headless --editor --quit` to populate it (the generated wrapper does this automatically when `.godot/` is missing).
- Validator is intentionally written to NOT depend on `class_name` resolution (uses `Resource` base + `res.get("field")` duck-typing), so even if the cache is stale it still works.

## Anti-patterns to avoid

- ❌ Using CSV/JSON/YAML loaders at runtime — Godot's native `.tres` is already text, git-friendly, type-safe, and Inspector-editable.
- ❌ Putting everything in one god-resource — harder to diff, no grouping, single-file merge conflicts.
- ❌ Hardcoding defaults in the Resource script AND in the `.tres` at different values — keep `.tres` authoritative; script defaults only act as fallback when a consumer never binds a resource.
- ❌ Reading `.tres` with `FileAccess` / `JSON.parse` — always use `load()` / `preload()`.

## Smoke-test before declaring done

Run `scripts/selftest.sh` (in this skill) which:
1. Creates a fresh temp Godot project.
2. Runs `scaffold.py` with every example spec.
3. Refreshes class cache + runs the validator.
4. Injects a bad value and confirms the validator now exits 1.
5. Cleans up.

```bash
bash ~/.codebuddy/skills/godot-data-driven-config/scripts/selftest.sh
```

## Deliverables checklist

When you finish, confirm ALL of:
- [ ] `res://data/specs/<name>.spec.json` exists and is committed
- [ ] `res://data/resources/<name>_data.gd` with `class_name` + typed `@export` fields
- [ ] `res://data/<name>s/default_<name>.tres` with sensible defaults
- [ ] `res://data/resources/data_manager.gd` exists and references the new category
- [ ] `project.godot` has `DataManager` in `[autoload]`
- [ ] Consumer `.gd` reference `<name>_data.xxx` (no more magic numbers)
- [ ] `bash tools/validate_data.sh` → exit 0
- [ ] `PROJECT_OVERVIEW.md` / `README.md` updated

## Files in this skill

```
SKILL.md                                  this file
QUICKREF.md                               one-page cheat sheet for the AI
schemas/field_spec.schema.json            JSON schema for designer-facing spec
templates/
  data_class.gd.tmpl                      Resource class template
  data_resource.tres.tmpl                 .tres template
  data_manager.gd.tmpl                    Autoload template (uses Resource base)
  validate_data.gd.tmpl                   CLI validator template (duck-typed)
  validate_data.sh.tmpl                   bash wrapper (exit-code fix-up)
scripts/
  scaffold.py                             end-to-end generator
  selftest.sh                             self-test / regression check
examples/
  weapon_spec.json
  enemy_spec.json
```

## 模块：godot-headless-verify

# Godot Headless Verify & Repair

> A pocket toolkit of **reproducible CLI recipes** for Godot 4 projects.
> Every recipe here is a copy-paste-ready one-liner (or short script) that
> exercises the engine without opening the editor. Use these instead of
> asking the user "can you open the editor and…" — that's slower and
> lossy.

---

## 0. The one-binary convention

Every recipe assumes you can reach Godot via either `$GODOT` env var or
its standard macOS location. Prefix every command with:

```bash
GODOT="${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}"
```

On Linux / Windows, set `$GODOT` to your binary. **Never** hard-code
`godot4` or `/opt/godot/...` in scripts — it breaks across machines.

---

## 1. Recipe: cache clean (safe)

**When**: editor shows `Cannot open file 'res://…'` or
`referenced non-existent resource` *even though the file exists*, typically
after a refactor / folder rename / branch swap.

**Why**: `.godot/imported/` and `.godot/uid_cache.bin` remember pre-move
paths. Godot doesn't self-heal until you force a rebuild.

```bash
# Requires: editor closed.
cd <project-root>

# Safe cache reset — preserves window layout + per-file folding state.
rm -rf .godot/imported \
       .godot/uid_cache.bin \
       .godot/global_script_class_cache.cfg \
       .godot/scene_groups_cache.cfg \
       .godot/editor/filesystem_cache* \
       .godot/editor/filesystem_update_* \
       .godot/editor/filesystem_update[0-9]*
# (zsh note: use `setopt NULL_GLOB` or run in bash if the * patterns
#  don't match anything and zsh complains)

# Rebuild cache headlessly (takes 30s-2min depending on project size).
"$GODOT" --headless --import --path .
```

**Keep these** (do NOT rm):
- `.godot/shader_cache/` — compiled shaders, expensive to rebuild
- `.godot/editor/*-folding-*.cfg` — per-file UI state
- `.godot/editor/editor_layout.cfg` — window layout

---

## 2. Recipe: scene-load smoke test

**When**: you just refactored something and want a 5-second "does it still
load?" answer before bothering with the full editor.

```bash
cat > /tmp/smoke.gd <<'EOF'
extends SceneTree

# Edit the paths you want to smoke-test:
const SCENES := [
    "res://scenes/boot/main.tscn",
    "res://scenes/levels/arena/arena.tscn",
    "res://scenes/levels/forest/forest.tscn",
]

func _initialize() -> void:
    var failed := 0
    for s in SCENES:
        var ps := load(s) as PackedScene
        if ps == null:
            push_error("FAIL load: %s" % s); failed += 1; continue
        var inst := ps.instantiate()
        if inst == null:
            push_error("FAIL instantiate: %s" % s); failed += 1; continue
        print("OK %s (children=%d)" % [s, inst.get_child_count()])
        inst.queue_free()
    quit(0 if failed == 0 else 1)
EOF

GODOT="${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}"
"$GODOT" --headless --path . --script /tmp/smoke.gd \
    2>&1 | grep -E 'ERROR|OK '

rm -f /tmp/smoke.gd
```

**Exit code** is 0 iff every scene loaded. Good for CI.

**Important**: `/tmp/smoke.gd` is outside the project, so Godot can't
resolve `res://` in its own script path. Always pass the full `/tmp/...`
filesystem path via `--script`. Don't put it inside `tools/` without the
matching `.uid` sidecar (pre-commit hook will otherwise complain).

---

## 3. Recipe: script-only parse check

**When**: you edited a bunch of `.gd` files and want to confirm they all
parse without opening the editor.

```bash
# --check-only runs the GDScript parser over all scripts the project
# touches; no scene is instantiated.
"$GODOT" --headless --quit --path . 2>&1 \
    | grep -iE 'SCRIPT ERROR|Parse Error' || echo "all scripts parse OK"
```

Note: `--quit` without a script exits after the engine's first idle frame,
which is enough to trigger script preloading.

---

## 4. Recipe: forced reimport of one folder

**When**: one specific asset got stuck with stale `.import` data but you
don't want a full project reimport.

```bash
# Delete just the .import files under the folder you care about.
# Godot will re-generate them on the next editor open OR headless --import.
find art/models/environment/arena -name '*.import' -delete

"$GODOT" --headless --import --path .
```

Pairs well with the `godot-asset-path-surgery` skill.

---

## 5. Recipe: run an arbitrary maintenance script

**When**: you want to batch-operate on resources (resave, audit, migrate).

Create the script under `tools/` so it's git-tracked and follows the
project's asset-structure rules. Template:

```gdscript
# tools/do_thing.gd
extends SceneTree

## One-shot maintenance: <what this does>.
## Usage:
##   /Applications/Godot.app/Contents/MacOS/Godot --headless --quit \
##       --path . --script tools/do_thing.gd

func _initialize() -> void:
    # ... your work here ...
    # Prefer idempotent ops: the script should be safe to re-run.
    quit(0)  # or quit(1) on failure
```

Checklist before committing:
- [ ] Has a header comment saying what it does and why
- [ ] Is idempotent (safe to re-run) — or prints a warning if not
- [ ] Uses `ResourceLoader.CACHE_MODE_IGNORE` when mutating
- [ ] Uses `ResourceSaver.FLAG_COMPRESS` when saving binaries (.mesh /
      .material / compressed .res) unless you have a reason otherwise
- [ ] Run it once, verify, then **don't delete it** — keep as living
      documentation of the maintenance event
- [ ] After creation, run Godot headless once to generate its `.uid`
      sidecar, then `git add` both files

---

## 6. Recipe: export / build validation

**When**: about to ship, want to confirm export presets still work.

```bash
# List presets defined in export_presets.cfg
grep '^\[preset\.' export_presets.cfg

# Dry-run export (v4.x):
mkdir -p /tmp/godot-export-test
"$GODOT" --headless --export-debug "<preset-name>" \
    /tmp/godot-export-test/game.pck --path .
# Check exit code; inspect .pck size sanity; `rm -rf /tmp/godot-export-test`
```

---

## 7. Common WARNING / ERROR noise (safe to ignore)

| Message | Source | Action |
|---|---|---|
| `ObjectDB instances leaked at exit` | Godot 4.6 cleanup order | Ignore for headless one-shots |
| `WARNING: [fbx] ...` | FBX SDK chatter | Ignore unless it mentions your file |
| `WARNING: Physics interpolation ... possibly benign` | Player runtime-spawned before physics tick | Log as tech debt, ignore at runtime |
| First-run `ERROR: failed loading resource` for every scene on an empty cache | Cache still rebuilding | Re-run after `--import` completes |

If you see an error that's **not** in this table and **not** trivial,
escalate — don't just swallow it.

---

## 8. CI / automation one-liner

The most common "I want to gate my PR on headless validity":

```bash
#!/usr/bin/env bash
set -euo pipefail
GODOT="${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}"
cd "$(dirname "$0")/.."

# 1. Structure check (project-specific).
bash tools/check_asset_structure.sh

# 2. Data-table validation (if using godot-data-driven-config skill).
[ -f tools/validate_data.sh ] && bash tools/validate_data.sh

# 3. Scene smoke test.
"$GODOT" --headless --path . --script tools/smoke.gd

# 4. No stale WARNING/ERROR on first-party code.
"$GODOT" --headless --quit --path . 2>&1 \
    | grep -iE 'SCRIPT ERROR|Parse Error' \
    && { echo "first-party script errors detected"; exit 1; } \
    || echo "clean"
```

---

## Anti-patterns — don't do these

- ❌ **Deleting all of `.godot/`**: wipes `shader_cache/` too → next
  editor open takes 10+ minutes rebuilding shaders.
- ❌ **Running maintenance scripts while the editor is open**: the
  editor will race-save stale in-memory state back over your change.
  Always close the editor first.
- ❌ **Assuming `--quit` waits for the filesystem scan**: it doesn't.
  Use `--import` when you need a complete rescan.
- ❌ **Hard-coding `/Applications/Godot.app/...` in committed scripts**:
  use `${GODOT:-<default>}` so the script works on other machines.
- ❌ **Treating smoke-test output as structured**: it's stderr-heavy,
  always pipe through `grep -E 'ERROR|OK'` before asserting.

---

## Integration with other skills

- **`godot-asset-path-surgery`** — after running surgery, verify with
  this skill's §2 smoke test, then clear cache via §1 before reopening
  the editor.
- **`godot-data-driven-config`** — the validator it generates
  (`tools/validate_data.sh`) is a domain-specific version of §8.
- **`gdscript-codegen`** — after generating new scripts, §3 parse-check
  catches syntax issues before the user opens Godot.

## 模块：godot-tres-format

# Godot .tres 资源文件格式规范

> **用途**：让 AI 能够直接读写 Godot 资源文件  
> **版本**：v1.0 · 2026-04-24  
> **适用引擎**：Godot 4.x

---

## 核心原则

**Godot 资源文件是纯文本**，AI 可以直接通过 `write_to_file` 创建材质、形状、环境等资源。

---

## 一、文件结构

```
[gd_resource type="ResourceType" format=3 uid="uid://xxx"]

[resource]
property1 = value1
property2 = value2
```

---

## 二、材质资源 (StandardMaterial3D)

### 2.1 基础材质

```
[gd_resource type="StandardMaterial3D" format=3]

[resource]
albedo_color = Color(0.8, 0.2, 0.2, 1)
roughness = 0.8
metallic = 0.0
```

### 2.2 金属材质

```
[gd_resource type="StandardMaterial3D" format=3]

[resource]
albedo_color = Color(0.9, 0.9, 0.9, 1)
roughness = 0.3
metallic = 0.9
metallic_specular = 0.5
```

### 2.3 发光材质

```
[gd_resource type="StandardMaterial3D" format=3]

[resource]
albedo_color = Color(1, 0.8, 0, 1)
emission_enabled = true
emission = Color(1, 0.8, 0, 1)
emission_energy_multiplier = 3.0
```

### 2.4 透明材质

```
[gd_resource type="StandardMaterial3D" format=3]

[resource]
transparency = 1
albedo_color = Color(0.2, 0.5, 1, 0.5)
```

### 2.5 无光照材质

```
[gd_resource type="StandardMaterial3D" format=3]

[resource]
shading_mode = 0
albedo_color = Color(1, 1, 1, 1)
```

### 2.6 带纹理材质

```
[gd_resource type="StandardMaterial3D" load_steps=2 format=3]

[ext_resource type="Texture2D" path="res://textures/brick.png" id="1_albedo"]

[resource]
albedo_texture = ExtResource("1_albedo")
roughness = 0.9
```

---

## 三、常用材质属性参考

| 属性 | 类型 | 说明 |
|------|------|------|
| `albedo_color` | Color | 基础颜色 |
| `albedo_texture` | Texture2D | 颜色贴图 |
| `roughness` | float (0-1) | 粗糙度，0=光滑，1=粗糙 |
| `metallic` | float (0-1) | 金属度 |
| `metallic_specular` | float (0-1) | 金属高光 |
| `emission_enabled` | bool | 启用发光 |
| `emission` | Color | 发光颜色 |
| `emission_energy_multiplier` | float | 发光强度倍数 |
| `transparency` | int | 0=不透明, 1=Alpha, 2=预乘Alpha |
| `cull_mode` | int | 0=背面剔除, 1=正面剔除, 2=不剔除 |
| `shading_mode` | int | 0=无光照, 1=逐顶点, 2=逐像素(默认) |
| `normal_enabled` | bool | 启用法线贴图 |
| `normal_texture` | Texture2D | 法线贴图 |
| `normal_scale` | float | 法线强度 |

---

## 四、环境资源 (Environment)

### 4.1 基础室外环境

```
[gd_resource type="Environment" format=3]

[resource]
background_mode = 1
background_color = Color(0.4, 0.6, 0.9, 1)
ambient_light_source = 2
ambient_light_color = Color(0.5, 0.5, 0.6, 1)
ambient_light_energy = 0.5
tonemap_mode = 2
tonemap_white = 6.0
ssao_enabled = true
ssil_enabled = true
glow_enabled = true
```

### 4.2 室内环境

```
[gd_resource type="Environment" format=3]

[resource]
background_mode = 1
background_color = Color(0.1, 0.1, 0.15, 1)
ambient_light_source = 1
ambient_light_color = Color(0.3, 0.3, 0.35, 1)
ambient_light_energy = 0.3
ssao_enabled = true
ssao_intensity = 2.0
```

### 4.3 带天空盒环境

```
[gd_resource type="Environment" load_steps=2 format=3]

[sub_resource type="Sky" id="Sky_001"]
sky_material = SubResource("ProceduralSkyMaterial_001")

[sub_resource type="ProceduralSkyMaterial" id="ProceduralSkyMaterial_001"]
sky_top_color = Color(0.3, 0.5, 0.9, 1)
sky_horizon_color = Color(0.7, 0.8, 0.95, 1)
ground_bottom_color = Color(0.2, 0.2, 0.2, 1)
ground_horizon_color = Color(0.5, 0.5, 0.5, 1)
sun_angle_max = 30.0

[resource]
background_mode = 2
sky = SubResource("Sky_001")
ambient_light_source = 3
tonemap_mode = 2
```

---

## 五、物理材质 (PhysicsMaterial)

```
[gd_resource type="PhysicsMaterial" format=3]

[resource]
friction = 0.8
rough = true
bounce = 0.2
absorbent = false
```

| 属性 | 说明 |
|------|------|
| `friction` | 摩擦力 (0-1) |
| `rough` | 粗糙模式 |
| `bounce` | 弹性 (0-1) |
| `absorbent` | 吸收模式 |

---

## 六、渐变资源 (Gradient)

### 6.1 线性渐变

```
[gd_resource type="Gradient" format=3]

[resource]
offsets = PackedFloat32Array(0, 0.5, 1)
colors = PackedColorArray(1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1)
```

### 6.2 用于粒子的渐变

```
[gd_resource type="Gradient" format=3]

[resource]
offsets = PackedFloat32Array(0, 0.3, 0.7, 1)
colors = PackedColorArray(1, 1, 1, 1, 1, 0.8, 0.2, 1, 1, 0.2, 0, 0.5, 0.5, 0.1, 0, 0)
```

---

## 七、曲线资源 (Curve)

### 7.1 基础曲线

```
[gd_resource type="Curve" format=3]

[resource]
min_value = 0.0
max_value = 1.0
_data = [Vector2(0, 0), 0.0, 0.0, 0, 0, Vector2(0.5, 1), 0.0, 0.0, 0, 0, Vector2(1, 0), 0.0, 0.0, 0, 0]
point_count = 3
```

### 7.2 淡入淡出曲线

```
[gd_resource type="Curve" format=3]

[resource]
_data = [Vector2(0, 0), 0.0, 2.0, 0, 1, Vector2(0.2, 1), 0.0, 0.0, 0, 0, Vector2(0.8, 1), 0.0, 0.0, 0, 0, Vector2(1, 0), -2.0, 0.0, 1, 0]
point_count = 4
```

---

## 八、样式盒资源 (StyleBox)

### 8.1 扁平样式盒

```
[gd_resource type="StyleBoxFlat" format=3]

[resource]
bg_color = Color(0.2, 0.2, 0.25, 1)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.4, 0.4, 0.5, 1)
corner_radius_top_left = 8
corner_radius_top_right = 8
corner_radius_bottom_right = 8
corner_radius_bottom_left = 8
```

### 8.2 按钮样式

```
[gd_resource type="StyleBoxFlat" format=3]

[resource]
bg_color = Color(0.3, 0.5, 0.8, 1)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4
shadow_color = Color(0, 0, 0, 0.3)
shadow_size = 2
shadow_offset = Vector2(0, 2)
```

---

## 九、着色器材质 (ShaderMaterial)

### 9.1 内联着色器

```
[gd_resource type="ShaderMaterial" load_steps=2 format=3]

[sub_resource type="Shader" id="Shader_001"]
code = "shader_type spatial;

uniform vec4 albedo_color : source_color = vec4(1.0);
uniform float metallic : hint_range(0, 1) = 0.0;

void fragment() {
    ALBEDO = albedo_color.rgb;
    METALLIC = metallic;
}
"

[resource]
shader = SubResource("Shader_001")
shader_parameter/albedo_color = Color(1, 0, 0, 1)
shader_parameter/metallic = 0.5
```

### 9.2 引用外部着色器

```
[gd_resource type="ShaderMaterial" load_steps=2 format=3]

[ext_resource type="Shader" path="res://shaders/custom.gdshader" id="1_shader"]

[resource]
shader = ExtResource("1_shader")
shader_parameter/speed = 2.0
shader_parameter/amplitude = 0.1
```

---

## 十、动画资源 (Animation)

### 10.1 简单位置动画

```
[gd_resource type="Animation" format=3]

[resource]
resource_name = "move_right"
length = 1.0
loop_mode = 0
tracks/0/type = "value"
tracks/0/imported = false
tracks/0/enabled = true
tracks/0/path = NodePath(".:position")
tracks/0/interp = 1
tracks/0/loop_wrap = true
tracks/0/keys = {
"times": PackedFloat32Array(0, 1),
"transitions": PackedFloat32Array(1, 1),
"update": 0,
"values": [Vector3(0, 0, 0), Vector3(5, 0, 0)]
}
```

### 10.2 颜色动画

```
[gd_resource type="Animation" format=3]

[resource]
resource_name = "flash_red"
length = 0.5
tracks/0/type = "value"
tracks/0/path = NodePath("MeshInstance3D:material_override:albedo_color")
tracks/0/keys = {
"times": PackedFloat32Array(0, 0.1, 0.5),
"values": [Color(1, 1, 1, 1), Color(1, 0, 0, 1), Color(1, 1, 1, 1)]
}
```

---

## 十一、字体资源 (FontFile)

字体通常是导入的，但可以创建 FontVariation：

```
[gd_resource type="FontVariation" load_steps=2 format=3]

[ext_resource type="FontFile" path="res://fonts/main.ttf" id="1_font"]

[resource]
base_font = ExtResource("1_font")
variation_opentype = {
"wght": 700
}
spacing_glyph = 2
spacing_top = -2
```

---

## 十二、粒子材质 (ParticleProcessMaterial)

```
[gd_resource type="ParticleProcessMaterial" format=3]

[resource]
emission_shape = 1
emission_sphere_radius = 0.5
direction = Vector3(0, 1, 0)
spread = 30.0
initial_velocity_min = 5.0
initial_velocity_max = 10.0
gravity = Vector3(0, -9.8, 0)
scale_min = 0.5
scale_max = 1.5
color = Color(1, 0.8, 0, 1)
```

---

## 十三、AI 操作指南

### 13.1 创建材质

```python
write_to_file("res://resources/enemy_mat.tres", """
[gd_resource type="StandardMaterial3D" format=3]

[resource]
albedo_color = Color(0.8, 0.2, 0.2, 1)
roughness = 0.7
emission_enabled = true
emission = Color(0.3, 0, 0, 1)
emission_energy_multiplier = 0.5
""")
```

### 13.2 创建环境

```python
write_to_file("res://resources/game_env.tres", """
[gd_resource type="Environment" format=3]

[resource]
background_mode = 1
background_color = Color(0.05, 0.05, 0.1, 1)
ambient_light_color = Color(0.2, 0.2, 0.3, 1)
ambient_light_energy = 0.5
ssao_enabled = true
glow_enabled = true
glow_intensity = 0.5
""")
```

### 13.3 创建物理材质

```python
write_to_file("res://resources/bouncy.tres", """
[gd_resource type="PhysicsMaterial" format=3]

[resource]
friction = 0.3
bounce = 0.9
""")
```

---

## 十四、资源类型速查表

| 类型 | 用途 | 文件 |
|------|------|------|
| `StandardMaterial3D` | 3D 材质 | `*.tres` |
| `CanvasItemMaterial` | 2D 材质 | `*.tres` |
| `ShaderMaterial` | 自定义着色器材质 | `*.tres` |
| `Environment` | 环境设置 | `*.tres` |
| `PhysicsMaterial` | 物理材质 | `*.tres` |
| `Gradient` | 渐变 | `*.tres` |
| `Curve` | 曲线 | `*.tres` |
| `StyleBoxFlat` | UI 样式盒 | `*.tres` |
| `ParticleProcessMaterial` | 粒子材质 | `*.tres` |
| `Animation` | 动画 | `*.tres` 或 `*.anim` |
| `AudioBusLayout` | 音频总线布局 | `*.tres` |
| `Theme` | UI 主题 | `*.tres` |

---

## 十五、颜色速查表

### 常用颜色

```
# 基础色
红色: Color(1, 0, 0, 1)
绿色: Color(0, 1, 0, 1)
蓝色: Color(0, 0, 1, 1)
白色: Color(1, 1, 1, 1)
黑色: Color(0, 0, 0, 1)

# 游戏常用
生命条红: Color(0.9, 0.2, 0.2, 1)
能量条蓝: Color(0.2, 0.5, 0.9, 1)
金币黄: Color(1, 0.85, 0, 1)
毒药绿: Color(0.3, 0.9, 0.2, 1)
暗紫色: Color(0.5, 0.2, 0.7, 1)

# UI 色
暗灰背景: Color(0.15, 0.15, 0.2, 1)
边框灰: Color(0.4, 0.4, 0.5, 1)
高亮蓝: Color(0.3, 0.6, 1, 1)
警告橙: Color(1, 0.6, 0.2, 1)
错误红: Color(0.9, 0.3, 0.3, 1)
成功绿: Color(0.3, 0.8, 0.4, 1)
```

## 模块：godot-tscn-format

# Godot .tscn 场景文件格式规范

> **用途**：让 AI 能够直接读写 Godot 场景文件  
> **版本**：v1.0 · 2026-04-24  
> **适用引擎**：Godot 4.x

---

## 核心原则

**Godot 场景文件是纯文本**，AI 可以直接通过 `write_to_file` 和 `replace_in_file` 操作，无需任何中间层。

---

## 一、文件结构总览

```
[gd_scene load_steps=N format=3 uid="uid://xxx"]    ← 头部（必需）

[ext_resource type="Type" path="res://..." id="ID"]  ← 外部资源引用（可选）
[ext_resource ...]

[sub_resource type="Type" id="ID"]                   ← 内嵌资源定义（可选）
property = value
[sub_resource ...]

[node name="Name" type="Type"]                       ← 根节点（必需）
property = value

[node name="Child" type="Type" parent="."]           ← 子节点
property = value

[connection signal="sig" from="Node" to="Target" method="func"]  ← 信号连接（可选）
```

---

## 二、头部声明

### 2.1 基本格式

```
[gd_scene load_steps=4 format=3]
```

| 字段 | 说明 |
|------|------|
| `load_steps` | 资源加载步数 = ext_resource 数 + sub_resource 数 + 1（场景本身） |
| `format` | 固定为 `3`（Godot 4.x） |
| `uid` | 可选，Godot 自动生成的唯一 ID，创建时可省略 |

### 2.2 计算 load_steps

```python
load_steps = len(ext_resources) + len(sub_resources) + 1
```

示例：2 个外部资源 + 3 个内嵌资源 → `load_steps=6`

---

## 三、外部资源引用 (ext_resource)

### 3.1 格式

```
[ext_resource type="Type" path="res://path/to/file" id="ID"]
```

### 3.2 常见类型

| type | 文件类型 | 示例 |
|------|----------|------|
| `Script` | GDScript | `path="res://scripts/player.gd"` |
| `PackedScene` | 场景 | `path="res://scenes/enemy.tscn"` |
| `Material` | 材质资源 | `path="res://materials/floor.tres"` |
| `Texture2D` | 2D 纹理 | `path="res://textures/icon.png"` |
| `AudioStream` | 音频 | `path="res://audio/shoot.wav"` |
| `Shader` | 着色器 | `path="res://shaders/outline.gdshader"` |

### 3.3 ID 命名规范

AI 生成时使用有意义的 ID：
```
[ext_resource type="Script" path="res://scripts/player.gd" id="1_player_script"]
[ext_resource type="Material" path="res://resources/floor_mat.tres" id="2_floor_mat"]
[ext_resource type="PackedScene" path="res://scenes/bullet.tscn" id="3_bullet_scene"]
```

---

## 四、内嵌资源定义 (sub_resource)

### 4.1 格式

```
[sub_resource type="Type" id="ID"]
property1 = value1
property2 = value2
```

### 4.2 常用碰撞形状

```
# 胶囊体（角色常用）
[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]
radius = 0.35
height = 1.8

# 球体
[sub_resource type="SphereShape3D" id="SphereShape3D_001"]
radius = 0.5

# 盒子
[sub_resource type="BoxShape3D" id="BoxShape3D_floor"]
size = Vector3(10, 0.2, 10)

# 圆柱体
[sub_resource type="CylinderShape3D" id="CylinderShape3D_001"]
height = 2.0
radius = 0.5

# 2D 形状
[sub_resource type="RectangleShape2D" id="RectangleShape2D_001"]
size = Vector2(32, 32)

[sub_resource type="CircleShape2D" id="CircleShape2D_001"]
radius = 16.0
```

### 4.3 常用网格

```
# 盒子网格
[sub_resource type="BoxMesh" id="BoxMesh_001"]
size = Vector3(1, 1, 1)

# 球体网格
[sub_resource type="SphereMesh" id="SphereMesh_001"]
radius = 0.5
height = 1.0

# 胶囊网格
[sub_resource type="CapsuleMesh" id="CapsuleMesh_001"]
radius = 0.5
height = 2.0

# 圆柱网格
[sub_resource type="CylinderMesh" id="CylinderMesh_001"]
top_radius = 0.5
bottom_radius = 0.5
height = 2.0

# 平面网格
[sub_resource type="PlaneMesh" id="PlaneMesh_001"]
size = Vector2(10, 10)
```

### 4.4 材质（内嵌）

```
[sub_resource type="StandardMaterial3D" id="Material_red"]
albedo_color = Color(1, 0, 0, 1)
roughness = 0.8
metallic = 0.2

# 发光材质
[sub_resource type="StandardMaterial3D" id="Material_glow"]
emission_enabled = true
emission = Color(1, 0.8, 0, 1)
emission_energy_multiplier = 2.0
```

---

## 五、节点声明 (node)

### 5.1 根节点

```
[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_player_script")
```

### 5.2 子节点

```
[node name="ChildName" type="NodeType" parent="."]
property = value
```

| parent 值 | 含义 |
|-----------|------|
| `.` | 直接子节点（父节点是根） |
| `ParentName` | 指定父节点名 |
| `Parent/Child` | 嵌套路径 |

### 5.3 引用资源

```
# 引用外部资源
script = ExtResource("1_player_script")
mesh = ExtResource("2_mesh")

# 引用内嵌资源
shape = SubResource("CapsuleShape3D_player")
mesh = SubResource("BoxMesh_001")
```

### 5.4 实例化场景

```
[node name="Enemy1" parent="Enemies" instance=ExtResource("4_enemy_scene")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 0, -10)
```

---

## 六、Transform 变换

### 6.1 Transform3D 格式

```
transform = Transform3D(bx.x, bx.y, bx.z, by.x, by.y, by.z, bz.x, bz.y, bz.z, ox, oy, oz)
```

| 参数 | 含义 |
|------|------|
| bx (1-3) | X 轴基向量 |
| by (4-6) | Y 轴基向量 |
| bz (7-9) | Z 轴基向量 |
| o (10-12) | 位置 (origin) |

### 6.2 常用变换

```
# 单位变换（默认位置）
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

# 仅位置
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 2, -10)

# 位置 + 缩放 0.5
transform = Transform3D(0.5, 0, 0, 0, 0.5, 0, 0, 0, 0.5, 5, 2, -10)

# 绕 Y 轴旋转 90°（sin90=1, cos90=0）
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0, 0)
```

### 6.3 Transform2D 格式

```
transform = Transform2D(cos, sin, -sin, cos, x, y)

# 单位变换
transform = Transform2D(1, 0, 0, 1, 100, 200)

# 旋转 45° 位于 (100, 200)
transform = Transform2D(0.707, 0.707, -0.707, 0.707, 100, 200)
```

---

## 七、常用属性值格式

### 7.1 基础类型

```
# 布尔
visible = true
enabled = false

# 整数
health = 100

# 浮点
speed = 10.5

# 字符串
name = "Player"
```

### 7.2 向量

```
# Vector2
position = Vector2(100, 200)
size = Vector2(32, 32)

# Vector3
position = Vector3(0, 1.5, 0)
target_position = Vector3(0, 0, -100)

# Vector4
custom_data = Vector4(1, 2, 3, 4)
```

### 7.3 颜色

```
# Color(R, G, B, A) 范围 0.0-1.0
light_color = Color(1, 0.85, 0.3, 1)
albedo_color = Color(0.25, 0.25, 0.3, 1)

# 半透明
modulate = Color(1, 1, 1, 0.5)
```

### 7.4 数组

```
# PackedStringArray
config/features = PackedStringArray("4.6", "Forward Plus")

# PackedVector2Array
polygon = PackedVector2Array(0, 0, 100, 0, 100, 100, 0, 100)

# 普通数组
groups = ["enemy", "damageable"]
```

---

## 八、信号连接 (connection)

### 8.1 格式

```
[connection signal="signal_name" from="NodePath" to="TargetPath" method="method_name"]
```

### 8.2 示例

```
# 同级节点连接
[connection signal="timeout" from="ShootCooldown" to="." method="_on_shoot_cooldown_timeout"]

# 子节点连接到根
[connection signal="body_entered" from="HitArea" to="." method="_on_hit_area_body_entered"]

# 带 flags
[connection signal="pressed" from="Button" to="." method="_on_button_pressed" flags=1]
```

---

## 九、完整示例模板

### 9.1 3D 角色场景

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://scripts/player.gd" id="1_script"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_001"]
radius = 0.35
height = 1.8

[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("CapsuleShape3D_001")

[node name="Camera3D" type="Camera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
fov = 75.0

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
```

### 9.2 2D 角色场景

```
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://scripts/player_2d.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://sprites/player.png" id="2_texture"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_001"]
size = Vector2(32, 48)

[node name="Player" type="CharacterBody2D"]
script = ExtResource("1_script")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_texture")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_001")
```

### 9.3 UI 场景

```
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/hud.gd" id="1_script"]

[node name="HUD" type="CanvasLayer"]
script = ExtResource("1_script")

[node name="MarginContainer" type="MarginContainer" parent="."]
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 20.0
offset_top = 20.0
offset_right = -20.0
offset_bottom = -20.0

[node name="VBoxContainer" type="VBoxContainer" parent="MarginContainer"]
layout_mode = 2

[node name="ScoreLabel" type="Label" parent="MarginContainer/VBoxContainer"]
layout_mode = 2
text = "Score: 0"

[node name="TimeLabel" type="Label" parent="MarginContainer/VBoxContainer"]
layout_mode = 2
text = "Time: 60"
```

---

## 十、AI 操作指南

### 10.1 创建新场景

```python
# AI 直接使用 write_to_file
write_to_file("res://scenes/new_scene.tscn", """
[gd_scene load_steps=1 format=3]

[node name="Root" type="Node3D"]
""")
```

### 10.2 修改现有场景

```python
# 使用 replace_in_file 修改属性
replace_in_file("res://scenes/player.tscn",
    old_str='fov = 75.0',
    new_str='fov = 90.0'
)
```

### 10.3 添加节点

```python
# 在场景末尾添加节点（信号连接之前）
replace_in_file("res://scenes/player.tscn",
    old_str='[connection signal=',
    new_str='''[node name="NewChild" type="Node3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

[connection signal='''
)
```

### 10.4 常见错误排查

| 错误 | 原因 | 修复 |
|------|------|------|
| `load_steps` 不匹配 | 资源数计算错误 | 重新计算 ext + sub + 1 |
| `id not found` | 引用了不存在的资源 ID | 检查 ExtResource/SubResource ID |
| 场景无法加载 | parent 路径错误 | 检查节点层级关系 |
| 属性无效 | 类型拼写错误 | 查阅 Godot 文档确认属性名 |

---

## 十一、快速参考

### 常用节点类型

| 类别 | 3D | 2D |
|------|-----|-----|
| 基础 | Node3D | Node2D |
| 物理角色 | CharacterBody3D | CharacterBody2D |
| 刚体 | RigidBody3D | RigidBody2D |
| 静态体 | StaticBody3D | StaticBody2D |
| 碰撞形状 | CollisionShape3D | CollisionShape2D |
| 网格 | MeshInstance3D | - |
| 精灵 | - | Sprite2D |
| 相机 | Camera3D | Camera2D |
| 灯光 | DirectionalLight3D, OmniLight3D, SpotLight3D | PointLight2D, DirectionalLight2D |

### 常用 UI 节点

| 节点 | 用途 |
|------|------|
| Control | UI 基类 |
| CanvasLayer | UI 层 |
| Label | 文本 |
| Button | 按钮 |
| TextureRect | 图片 |
| ProgressBar | 进度条 |
| VBoxContainer / HBoxContainer | 布局容器 |
| MarginContainer | 边距容器 |

## 模块：godot-utils

# GDScript 工具函数库

> **用途**：提供可复用的 GDScript 工具函数，加速游戏开发  
> **版本**：v1.0 · 2026-04-24  
> **适用**：Godot 4.x

---

## 目录

1. [数学工具](#1-数学工具)
2. [向量工具](#2-向量工具)
3. [随机工具](#3-随机工具)
4. [时间工具](#4-时间工具)
5. [字符串工具](#5-字符串工具)
6. [数组工具](#6-数组工具)
7. [节点工具](#7-节点工具)
8. [文件工具](#8-文件工具)
9. [调试工具](#9-调试工具)
10. [缓动工具](#10-缓动工具)

---

## 使用方式

### 方式 1：复制到项目
直接复制需要的函数到你的脚本中。

### 方式 2：Autoload
创建 `res://autoload/utils.gd`，在项目设置中注册为 Autoload（名称 `Utils`），然后全局调用 `Utils.xxx()`。

---

## 1. 数学工具

```gdscript
class_name MathUtils

## 线性插值，支持 clamp
static func lerp_clamped(from: float, to: float, weight: float) -> float:
    return lerpf(from, to, clampf(weight, 0.0, 1.0))

## 平滑阻尼（类似 Unity 的 SmoothDamp）
static func smooth_damp(current: float, target: float, velocity: float, smooth_time: float, delta: float) -> Array:
    var omega := 2.0 / smooth_time
    var x := omega * delta
    var exp_factor := 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
    var change := current - target
    var temp := (velocity + omega * change) * delta
    var new_velocity := (velocity - omega * temp) * exp_factor
    var new_value := target + (change + temp) * exp_factor
    return [new_value, new_velocity]

## 重映射值从一个范围到另一个范围
static func remap(value: float, from_min: float, from_max: float, to_min: float, to_max: float) -> float:
    return to_min + (value - from_min) * (to_max - to_min) / (from_max - from_min)

## 重映射并 clamp
static func remap_clamped(value: float, from_min: float, from_max: float, to_min: float, to_max: float) -> float:
    var t := clampf((value - from_min) / (from_max - from_min), 0.0, 1.0)
    return lerpf(to_min, to_max, t)

## 角度归一化到 [-180, 180]
static func normalize_angle(degrees: float) -> float:
    degrees = fmod(degrees + 180.0, 360.0)
    if degrees < 0:
        degrees += 360.0
    return degrees - 180.0

## 角度归一化到 [0, 360]
static func normalize_angle_positive(degrees: float) -> float:
    degrees = fmod(degrees, 360.0)
    if degrees < 0:
        degrees += 360.0
    return degrees

## 弧度归一化到 [-PI, PI]
static func normalize_radians(radians: float) -> float:
    radians = fmod(radians + PI, TAU)
    if radians < 0:
        radians += TAU
    return radians - PI

## 检查两个浮点数是否近似相等
static func approx_equal(a: float, b: float, epsilon := 0.0001) -> bool:
    return absf(a - b) < epsilon

## 检查值是否在范围内
static func in_range(value: float, min_val: float, max_val: float) -> bool:
    return value >= min_val and value <= max_val

## 取模（支持负数，结果总是正数）
static func positive_mod(a: int, b: int) -> int:
    return ((a % b) + b) % b

## 取模浮点版
static func positive_fmod(a: float, b: float) -> float:
    return fmod(fmod(a, b) + b, b)
```

---

## 2. 向量工具

```gdscript
class_name VectorUtils

## Vector2 平滑阻尼
static func smooth_damp_v2(current: Vector2, target: Vector2, velocity: Vector2, smooth_time: float, delta: float) -> Array:
    var result_x := MathUtils.smooth_damp(current.x, target.x, velocity.x, smooth_time, delta)
    var result_y := MathUtils.smooth_damp(current.y, target.y, velocity.y, smooth_time, delta)
    return [Vector2(result_x[0], result_y[0]), Vector2(result_x[1], result_y[1])]

## Vector3 平滑阻尼
static func smooth_damp_v3(current: Vector3, target: Vector3, velocity: Vector3, smooth_time: float, delta: float) -> Array:
    var result_x := MathUtils.smooth_damp(current.x, target.x, velocity.x, smooth_time, delta)
    var result_y := MathUtils.smooth_damp(current.y, target.y, velocity.y, smooth_time, delta)
    var result_z := MathUtils.smooth_damp(current.z, target.z, velocity.z, smooth_time, delta)
    return [Vector3(result_x[0], result_y[0], result_z[0]), Vector3(result_x[1], result_y[1], result_z[1])]

## 获取 Vector2 的垂直向量（顺时针）
static func perpendicular_cw(v: Vector2) -> Vector2:
    return Vector2(v.y, -v.x)

## 获取 Vector2 的垂直向量（逆时针）
static func perpendicular_ccw(v: Vector2) -> Vector2:
    return Vector2(-v.y, v.x)

## 将 Vector2 旋转指定角度（弧度）
static func rotate_v2(v: Vector2, radians: float) -> Vector2:
    return v.rotated(radians)

## 计算两个向量之间的有符号角度（弧度，-PI 到 PI）
static func signed_angle(from: Vector2, to: Vector2) -> float:
    return atan2(from.cross(to), from.dot(to))

## 3D 世界坐标转 2D 俯视坐标 (Y 轴向上时)
static func world_to_top_down(world_pos: Vector3) -> Vector2:
    return Vector2(world_pos.x, world_pos.z)

## 2D 俯视坐标转 3D 世界坐标 (指定高度)
static func top_down_to_world(pos_2d: Vector2, height := 0.0) -> Vector3:
    return Vector3(pos_2d.x, height, pos_2d.y)

## 计算点到线段的最近点
static func closest_point_on_segment(point: Vector2, seg_start: Vector2, seg_end: Vector2) -> Vector2:
    var seg := seg_end - seg_start
    var len_sq := seg.length_squared()
    if len_sq < 0.0001:
        return seg_start
    var t := clampf((point - seg_start).dot(seg) / len_sq, 0.0, 1.0)
    return seg_start + seg * t

## 计算点到线段的距离
static func distance_to_segment(point: Vector2, seg_start: Vector2, seg_end: Vector2) -> float:
    return point.distance_to(closest_point_on_segment(point, seg_start, seg_end))

## 限制向量长度
static func clamp_length(v: Vector2, max_length: float) -> Vector2:
    if v.length_squared() > max_length * max_length:
        return v.normalized() * max_length
    return v

## Vector3 版本
static func clamp_length_v3(v: Vector3, max_length: float) -> Vector3:
    if v.length_squared() > max_length * max_length:
        return v.normalized() * max_length
    return v
```

---

## 3. 随机工具

```gdscript
class_name RandomUtils

## 从数组中随机选择一个元素
static func pick(arr: Array) -> Variant:
    if arr.is_empty():
        return null
    return arr[randi() % arr.size()]

## 从数组中随机选择 N 个不重复元素
static func pick_n(arr: Array, n: int) -> Array:
    var shuffled := arr.duplicate()
    shuffled.shuffle()
    return shuffled.slice(0, mini(n, shuffled.size()))

## 带权重随机选择
static func pick_weighted(items: Array, weights: Array[float]) -> Variant:
    if items.is_empty() or items.size() != weights.size():
        return null
    
    var total := 0.0
    for w in weights:
        total += w
    
    var r := randf() * total
    var cumulative := 0.0
    for i in items.size():
        cumulative += weights[i]
        if r <= cumulative:
            return items[i]
    
    return items[-1]

## 随机布尔值
static func random_bool(true_chance := 0.5) -> bool:
    return randf() < true_chance

## 随机范围内的整数
static func random_int(min_val: int, max_val: int) -> int:
    return randi_range(min_val, max_val)

## 随机范围内的浮点数
static func random_float(min_val: float, max_val: float) -> float:
    return randf_range(min_val, max_val)

## 随机单位圆内的点
static func random_in_circle(radius := 1.0) -> Vector2:
    var angle := randf() * TAU
    var r := sqrt(randf()) * radius  # sqrt 使分布均匀
    return Vector2(cos(angle), sin(angle)) * r

## 随机圆环上的点
static func random_on_circle(radius := 1.0) -> Vector2:
    var angle := randf() * TAU
    return Vector2(cos(angle), sin(angle)) * radius

## 随机单位球内的点
static func random_in_sphere(radius := 1.0) -> Vector3:
    var theta := randf() * TAU
    var phi := acos(2.0 * randf() - 1.0)
    var r := pow(randf(), 1.0/3.0) * radius
    return Vector3(
        r * sin(phi) * cos(theta),
        r * sin(phi) * sin(theta),
        r * cos(phi)
    )

## 随机球面上的点
static func random_on_sphere(radius := 1.0) -> Vector3:
    var theta := randf() * TAU
    var phi := acos(2.0 * randf() - 1.0)
    return Vector3(
        radius * sin(phi) * cos(theta),
        radius * sin(phi) * sin(theta),
        radius * cos(phi)
    )

## 高斯/正态分布随机数（Box-Muller 变换）
static func random_gaussian(mean := 0.0, std_dev := 1.0) -> float:
    var u1 := randf()
    var u2 := randf()
    var z := sqrt(-2.0 * log(u1)) * cos(TAU * u2)
    return mean + z * std_dev

## 随机颜色
static func random_color(alpha := 1.0) -> Color:
    return Color(randf(), randf(), randf(), alpha)

## 随机 HSV 颜色（更好看）
static func random_color_hsv(s_range := Vector2(0.5, 1.0), v_range := Vector2(0.5, 1.0), alpha := 1.0) -> Color:
    var h := randf()
    var s := randf_range(s_range.x, s_range.y)
    var v := randf_range(v_range.x, v_range.y)
    return Color.from_hsv(h, s, v, alpha)
```

---

## 4. 时间工具

```gdscript
class_name TimeUtils

## 格式化秒数为 MM:SS
static func format_time_mmss(total_seconds: float) -> String:
    var minutes := int(total_seconds) / 60
    var seconds := int(total_seconds) % 60
    return "%02d:%02d" % [minutes, seconds]

## 格式化秒数为 HH:MM:SS
static func format_time_hhmmss(total_seconds: float) -> String:
    var hours := int(total_seconds) / 3600
    var minutes := (int(total_seconds) % 3600) / 60
    var seconds := int(total_seconds) % 60
    return "%02d:%02d:%02d" % [hours, minutes, seconds]

## 格式化秒数为 MM:SS.mmm（含毫秒）
static func format_time_precise(total_seconds: float) -> String:
    var minutes := int(total_seconds) / 60
    var seconds := int(total_seconds) % 60
    var millis := int((total_seconds - int(total_seconds)) * 1000)
    return "%02d:%02d.%03d" % [minutes, seconds, millis]

## 解析 MM:SS 字符串为秒数
static func parse_time_mmss(time_str: String) -> float:
    var parts := time_str.split(":")
    if parts.size() != 2:
        return 0.0
    return float(parts[0]) * 60 + float(parts[1])

## 创建一次性定时器
static func create_timer(node: Node, duration: float, callback: Callable) -> SceneTreeTimer:
    var timer := node.get_tree().create_timer(duration)
    timer.timeout.connect(callback)
    return timer

## 等待指定时间（协程用）
static func wait(node: Node, duration: float) -> Signal:
    return node.get_tree().create_timer(duration).timeout
```

**使用示例**：
```gdscript
# 协程等待
await TimeUtils.wait(self, 1.5)
print("1.5 秒后执行")

# 一次性定时器
TimeUtils.create_timer(self, 2.0, func(): print("2 秒后执行"))
```

---

## 5. 字符串工具

```gdscript
class_name StringUtils

## 首字母大写
static func capitalize_first(s: String) -> String:
    if s.is_empty():
        return s
    return s[0].to_upper() + s.substr(1)

## 转换为 Title Case
static func to_title_case(s: String) -> String:
    var words := s.split(" ")
    var result := PackedStringArray()
    for word in words:
        result.append(capitalize_first(word.to_lower()))
    return " ".join(result)

## snake_case 转 PascalCase
static func snake_to_pascal(s: String) -> String:
    var parts := s.split("_")
    var result := ""
    for part in parts:
        result += capitalize_first(part)
    return result

## PascalCase 转 snake_case
static func pascal_to_snake(s: String) -> String:
    var result := ""
    for i in s.length():
        var c := s[i]
        if c == c.to_upper() and i > 0:
            result += "_"
        result += c.to_lower()
    return result

## 截断字符串（加省略号）
static func truncate(s: String, max_length: int, suffix := "...") -> String:
    if s.length() <= max_length:
        return s
    return s.substr(0, max_length - suffix.length()) + suffix

## 检查是否为有效的标识符（变量名）
static func is_valid_identifier(s: String) -> bool:
    if s.is_empty():
        return false
    var first := s[0]
    if not (first.is_valid_identifier() and not first.is_valid_int()):
        return false
    for i in range(1, s.length()):
        if not s[i].is_valid_identifier():
            return false
    return true

## 移除所有空白字符
static func remove_whitespace(s: String) -> String:
    return s.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

## 格式化数字（加千位分隔符）
static func format_number(n: int, separator := ",") -> String:
    var s := str(abs(n))
    var result := ""
    var count := 0
    for i in range(s.length() - 1, -1, -1):
        if count > 0 and count % 3 == 0:
            result = separator + result
        result = s[i] + result
        count += 1
    return ("-" if n < 0 else "") + result

## 重复字符串 N 次
static func repeat(s: String, times: int) -> String:
    var result := ""
    for i in times:
        result += s
    return result

## 安全获取子字符串
static func safe_substr(s: String, from: int, length := -1) -> String:
    if from < 0:
        from = 0
    if from >= s.length():
        return ""
    if length < 0:
        return s.substr(from)
    return s.substr(from, mini(length, s.length() - from))
```

---

## 6. 数组工具

```gdscript
class_name ArrayUtils

## 查找满足条件的第一个元素
static func find(arr: Array, predicate: Callable) -> Variant:
    for item in arr:
        if predicate.call(item):
            return item
    return null

## 查找满足条件的所有元素
static func filter(arr: Array, predicate: Callable) -> Array:
    var result := []
    for item in arr:
        if predicate.call(item):
            result.append(item)
    return result

## 映射数组
static func map(arr: Array, transform: Callable) -> Array:
    var result := []
    for item in arr:
        result.append(transform.call(item))
    return result

## 规约/折叠数组
static func reduce(arr: Array, accumulator: Callable, initial: Variant) -> Variant:
    var result := initial
    for item in arr:
        result = accumulator.call(result, item)
    return result

## 求和
static func sum(arr: Array) -> float:
    return reduce(arr, func(acc, x): return acc + x, 0.0)

## 求平均值
static func average(arr: Array) -> float:
    if arr.is_empty():
        return 0.0
    return sum(arr) / arr.size()

## 求最大值
static func max_value(arr: Array) -> Variant:
    if arr.is_empty():
        return null
    var result = arr[0]
    for i in range(1, arr.size()):
        if arr[i] > result:
            result = arr[i]
    return result

## 求最小值
static func min_value(arr: Array) -> Variant:
    if arr.is_empty():
        return null
    var result = arr[0]
    for i in range(1, arr.size()):
        if arr[i] < result:
            result = arr[i]
    return result

## 去重
static func unique(arr: Array) -> Array:
    var result := []
    for item in arr:
        if item not in result:
            result.append(item)
    return result

## 分块
static func chunk(arr: Array, size: int) -> Array[Array]:
    var result: Array[Array] = []
    var i := 0
    while i < arr.size():
        result.append(arr.slice(i, i + size))
        i += size
    return result

## 展平嵌套数组（一层）
static func flatten(arr: Array) -> Array:
    var result := []
    for item in arr:
        if item is Array:
            result.append_array(item)
        else:
            result.append(item)
    return result

## 数组差集（a - b）
static func difference(a: Array, b: Array) -> Array:
    var result := []
    for item in a:
        if item not in b:
            result.append(item)
    return result

## 数组交集
static func intersection(a: Array, b: Array) -> Array:
    var result := []
    for item in a:
        if item in b and item not in result:
            result.append(item)
    return result

## 检查所有元素是否满足条件
static func all(arr: Array, predicate: Callable) -> bool:
    for item in arr:
        if not predicate.call(item):
            return false
    return true

## 检查是否存在满足条件的元素
static func any(arr: Array, predicate: Callable) -> bool:
    for item in arr:
        if predicate.call(item):
            return true
    return false

## 计算满足条件的元素个数
static func count(arr: Array, predicate: Callable) -> int:
    var result := 0
    for item in arr:
        if predicate.call(item):
            result += 1
    return result
```

---

## 7. 节点工具

```gdscript
class_name NodeUtils

## 安全获取节点（不存在返回 null，不报错）
static func get_node_safe(from: Node, path: NodePath) -> Node:
    if from.has_node(path):
        return from.get_node(path)
    return null

## 递归查找第一个指定类型的子节点
static func find_child_of_type(node: Node, type: GDScript) -> Node:
    for child in node.get_children():
        if is_instance_of(child, type):
            return child
        var found := find_child_of_type(child, type)
        if found:
            return found
    return null

## 递归查找所有指定类型的子节点
static func find_children_of_type(node: Node, type: GDScript) -> Array[Node]:
    var result: Array[Node] = []
    for child in node.get_children():
        if is_instance_of(child, type):
            result.append(child)
        result.append_array(find_children_of_type(child, type))
    return result

## 获取节点到根的路径（调试用）
static func get_full_path(node: Node) -> String:
    var path := node.name
    var parent := node.get_parent()
    while parent:
        path = parent.name + "/" + path
        parent = parent.get_parent()
    return path

## 安全 queue_free（检查有效性）
static func safe_free(node: Node) -> void:
    if is_instance_valid(node):
        node.queue_free()

## 延迟调用（下一帧）
static func call_deferred_frame(node: Node, callback: Callable) -> void:
    node.get_tree().process_frame.connect(callback, CONNECT_ONE_SHOT)

## 移除节点的所有子节点
static func remove_all_children(node: Node) -> void:
    for child in node.get_children():
        child.queue_free()

## 重新设置父节点（保持世界位置）
static func reparent_keep_global(node: Node3D, new_parent: Node) -> void:
    var global_transform := node.global_transform
    node.get_parent().remove_child(node)
    new_parent.add_child(node)
    node.global_transform = global_transform

## 2D 版本
static func reparent_keep_global_2d(node: Node2D, new_parent: Node) -> void:
    var global_transform := node.global_transform
    node.get_parent().remove_child(node)
    new_parent.add_child(node)
    node.global_transform = global_transform

## 禁用/启用节点及其所有子节点的处理
static func set_process_recursive(node: Node, enabled: bool) -> void:
    node.set_process(enabled)
    node.set_physics_process(enabled)
    node.set_process_input(enabled)
    for child in node.get_children():
        set_process_recursive(child, enabled)
```

---

## 8. 文件工具

```gdscript
class_name FileUtils

## 检查文件是否存在
static func file_exists(path: String) -> bool:
    return FileAccess.file_exists(path)

## 检查目录是否存在
static func dir_exists(path: String) -> bool:
    return DirAccess.dir_exists_absolute(path)

## 读取文本文件
static func read_text(path: String) -> String:
    var file := FileAccess.open(path, FileAccess.READ)
    if file:
        return file.get_as_text()
    return ""

## 写入文本文件
static func write_text(path: String, content: String) -> bool:
    var file := FileAccess.open(path, FileAccess.WRITE)
    if file:
        file.store_string(content)
        return true
    return false

## 追加文本到文件
static func append_text(path: String, content: String) -> bool:
    var file := FileAccess.open(path, FileAccess.READ_WRITE)
    if file:
        file.seek_end()
        file.store_string(content)
        return true
    return false

## 读取 JSON 文件
static func read_json(path: String) -> Variant:
    var text := read_text(path)
    if text.is_empty():
        return null
    var json := JSON.new()
    if json.parse(text) == OK:
        return json.data
    return null

## 写入 JSON 文件
static func write_json(path: String, data: Variant, indent := "\t") -> bool:
    return write_text(path, JSON.stringify(data, indent))

## 获取目录下所有文件（递归可选）
static func list_files(dir_path: String, recursive := false, extension := "") -> PackedStringArray:
    var result := PackedStringArray()
    var dir := DirAccess.open(dir_path)
    if not dir:
        return result
    
    dir.list_dir_begin()
    var file_name := dir.get_next()
    while file_name != "":
        if file_name != "." and file_name != "..":
            var full_path := dir_path.path_join(file_name)
            if dir.current_is_dir():
                if recursive:
                    result.append_array(list_files(full_path, true, extension))
            else:
                if extension.is_empty() or file_name.ends_with(extension):
                    result.append(full_path)
        file_name = dir.get_next()
    
    return result

## 确保目录存在（递归创建）
static func ensure_dir(path: String) -> bool:
    if DirAccess.dir_exists_absolute(path):
        return true
    return DirAccess.make_dir_recursive_absolute(path) == OK

## 获取文件大小
static func get_file_size(path: String) -> int:
    var file := FileAccess.open(path, FileAccess.READ)
    if file:
        return file.get_length()
    return -1

## 复制文件
static func copy_file(from: String, to: String) -> bool:
    return DirAccess.copy_absolute(from, to) == OK

## 移动文件
static func move_file(from: String, to: String) -> bool:
    return DirAccess.rename_absolute(from, to) == OK

## 删除文件
static func delete_file(path: String) -> bool:
    return DirAccess.remove_absolute(path) == OK
```

---

## 9. 调试工具

```gdscript
class_name DebugUtils

## 打印带时间戳的日志
static func log(message: String) -> void:
    var time := Time.get_time_dict_from_system()
    print("[%02d:%02d:%02d] %s" % [time["hour"], time["minute"], time["second"], message])

## 打印变量名和值
static func print_var(name: String, value: Variant) -> void:
    print("%s = %s" % [name, str(value)])

## 打印分隔线
static func print_separator(char := "=", length := 50) -> void:
    print(StringUtils.repeat(char, length))

## 打印字典（格式化）
static func print_dict(d: Dictionary, indent := 0) -> void:
    var prefix := StringUtils.repeat("  ", indent)
    for key in d:
        var value = d[key]
        if value is Dictionary:
            print("%s%s:" % [prefix, key])
            print_dict(value, indent + 1)
        else:
            print("%s%s: %s" % [prefix, key, str(value)])

## 断言（调试版本有效）
static func assert_true(condition: bool, message := "Assertion failed") -> void:
    if OS.is_debug_build() and not condition:
        push_error(message)
        assert(false, message)

## 计时器开始
static var _timers := {}
static func timer_start(name: String) -> void:
    _timers[name] = Time.get_ticks_msec()

## 计时器结束并打印
static func timer_end(name: String) -> void:
    if name in _timers:
        var elapsed := Time.get_ticks_msec() - _timers[name]
        print("[TIMER] %s: %d ms" % [name, elapsed])
        _timers.erase(name)

## 性能计数（帧时间内调用次数）
static var _counters := {}
static var _counter_frame := 0
static func count(name: String) -> void:
    var frame := Engine.get_process_frames()
    if frame != _counter_frame:
        if not _counters.is_empty():
            print("[COUNTERS] Frame %d:" % _counter_frame)
            for key in _counters:
                print("  %s: %d" % [key, _counters[key]])
        _counters.clear()
        _counter_frame = frame
    _counters[name] = _counters.get(name, 0) + 1

## 绘制调试点（需要在 _draw 中调用）
static func draw_debug_point(canvas: CanvasItem, pos: Vector2, color := Color.RED, size := 5.0) -> void:
    canvas.draw_circle(pos, size, color)

## 绘制调试箭头
static func draw_debug_arrow(canvas: CanvasItem, from: Vector2, to: Vector2, color := Color.RED, width := 2.0) -> void:
    canvas.draw_line(from, to, color, width)
    var dir := (to - from).normalized()
    var perp := Vector2(-dir.y, dir.x)
    var arrow_size := 10.0
    canvas.draw_line(to, to - dir * arrow_size + perp * arrow_size * 0.5, color, width)
    canvas.draw_line(to, to - dir * arrow_size - perp * arrow_size * 0.5, color, width)
```

---

## 10. 缓动工具

```gdscript
class_name EaseUtils

## 常用缓动函数

static func ease_in_quad(t: float) -> float:
    return t * t

static func ease_out_quad(t: float) -> float:
    return 1.0 - (1.0 - t) * (1.0 - t)

static func ease_in_out_quad(t: float) -> float:
    return 2.0 * t * t if t < 0.5 else 1.0 - pow(-2.0 * t + 2.0, 2) / 2.0

static func ease_in_cubic(t: float) -> float:
    return t * t * t

static func ease_out_cubic(t: float) -> float:
    return 1.0 - pow(1.0 - t, 3)

static func ease_in_out_cubic(t: float) -> float:
    return 4.0 * t * t * t if t < 0.5 else 1.0 - pow(-2.0 * t + 2.0, 3) / 2.0

static func ease_in_elastic(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return -pow(2, 10 * t - 10) * sin((t * 10 - 10.75) * (TAU / 3))

static func ease_out_elastic(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return pow(2, -10 * t) * sin((t * 10 - 0.75) * (TAU / 3)) + 1

static func ease_out_bounce(t: float) -> float:
    const n1 := 7.5625
    const d1 := 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

static func ease_in_bounce(t: float) -> float:
    return 1 - ease_out_bounce(1 - t)

## 应用缓动到值
static func apply(from: float, to: float, t: float, ease_func: Callable) -> float:
    return lerpf(from, to, ease_func.call(clampf(t, 0.0, 1.0)))

## 应用缓动到 Vector2
static func apply_v2(from: Vector2, to: Vector2, t: float, ease_func: Callable) -> Vector2:
    var eased := ease_func.call(clampf(t, 0.0, 1.0))
    return from.lerp(to, eased)

## 应用缓动到 Vector3
static func apply_v3(from: Vector3, to: Vector3, t: float, ease_func: Callable) -> Vector3:
    var eased := ease_func.call(clampf(t, 0.0, 1.0))
    return from.lerp(to, eased)

## 应用缓动到 Color
static func apply_color(from: Color, to: Color, t: float, ease_func: Callable) -> Color:
    var eased := ease_func.call(clampf(t, 0.0, 1.0))
    return from.lerp(to, eased)
```

**使用示例**：
```gdscript
# 手动应用缓动
var progress := 0.0
func _process(delta: float) -> void:
    progress += delta * 0.5  # 2 秒完成
    position.x = EaseUtils.apply(0, 500, progress, EaseUtils.ease_out_elastic)

# 或者直接使用 Tween（内置缓动）
var tween := create_tween()
tween.tween_property(self, "position:x", 500, 2.0).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_ELASTIC)
```

---

## 完整 Autoload 脚本

如果你想一次性使用所有工具，可以创建一个合并的 Autoload：

```gdscript
# autoload/utils.gd
extends Node

# 导入所有工具类
const Math := preload("res://utils/math_utils.gd")
const Vector := preload("res://utils/vector_utils.gd")
const Random := preload("res://utils/random_utils.gd")
const Time := preload("res://utils/time_utils.gd")
const Str := preload("res://utils/string_utils.gd")
const Arr := preload("res://utils/array_utils.gd")
const Node := preload("res://utils/node_utils.gd")
const File := preload("res://utils/file_utils.gd")
const Debug := preload("res://utils/debug_utils.gd")
const Ease := preload("res://utils/ease_utils.gd")
```

然后这样使用：
```gdscript
var random_item = Utils.Random.pick(my_array)
var formatted = Utils.Str.format_number(1234567)
Utils.Debug.log("Something happened")
```

---

## 快速参考

| 工具类 | 常用函数 |
|--------|----------|
| MathUtils | `remap`, `normalize_angle`, `approx_equal` |
| VectorUtils | `smooth_damp_v2/v3`, `perpendicular_cw`, `world_to_top_down` |
| RandomUtils | `pick`, `pick_weighted`, `random_in_circle`, `random_gaussian` |
| TimeUtils | `format_time_mmss`, `create_timer`, `wait` |
| StringUtils | `truncate`, `format_number`, `snake_to_pascal` |
| ArrayUtils | `find`, `filter`, `map`, `reduce`, `unique` |
| NodeUtils | `find_child_of_type`, `safe_free`, `reparent_keep_global` |
| FileUtils | `read_json`, `write_json`, `list_files`, `ensure_dir` |
| DebugUtils | `log`, `timer_start/end`, `draw_debug_arrow` |
| EaseUtils | `ease_out_elastic`, `ease_out_bounce`, `apply` |

## 模块：safe-file-operations

# 🚨 安全文件操作规范（血泪教训版）

## 事故回顾

2026年4月19日，在 CodeBuddyPlugin 项目中，为了清理 `plugin/out/` 编译输出目录，
执行了 `rd /s /q` 命令，但由于 **PowerShell 与 cmd 语法混淆**，命令被错误解析，
导致 **整个项目目录被递归删除**，包括：

- `.git/` — 版本历史全部丢失
- `plugin/src/` — 所有 TypeScript 源码
- `server/` — 整个后端代码
- `package.json`、`tsconfig.json` — 项目配置
- `node_modules/` — 依赖
- `build.bat`、`install.bat` 等脚本
- `plugin/resources/icon.svg` — 刚刚精心制作的自定义图标

**整个项目从有到无，不可逆转。**

---

## 🔴 绝对禁止（NEVER DO）

### 1. 禁止使用 `rd /s /q`、`rm -rf`、`Remove-Item -Recurse -Force` 清理目录
- **永远不要**用这些命令来清理编译输出、临时文件
- 即使目标路径看起来正确，Shell 语法差异可能导致灾难
- PowerShell 中 `rd` 是 `Remove-Item` 的别名，行为与 cmd 的 `rd` **不完全相同**

### 2. 禁止在项目根目录附近执行任何递归删除命令
- 哪怕目标是子目录，一个路径解析错误就会删掉整个项目
- 尤其是包含空格、特殊字符、或使用变量拼接路径时

### 3. 禁止先删后建的文件操作模式
- 不要 `delete` + `write`，直接 `write_to_file` 覆盖即可
- `write_to_file` 本身就是覆盖语义，不需要先删除

---

## 🟢 正确做法（ALWAYS DO）

### 清理编译输出
```
# 正确：使用专用工具，不用终端命令
- 用 IDE 的 clean 命令
- 或手动删除 out/ 下的 .js 文件（不要删 out/ 目录本身）
- 如果必须用命令，先 `dir` / `ls` 确认目标内容
```

### 如果确实需要删除目录
1. **先 `ls` / `dir` 列出内容**，确认是预期的目标
2. **只删除文件，不删除目录结构**（用 `del /q out\*.js` 而非 `rd /s /q out`）
3. **使用 IDE 工具** (`delete_file`) 逐个删除，而非批量终端命令
4. **绝不在包含 .git 的目录层级使用递归删除**

### 文件修改
- 修改文件 → `replace_in_file`（精确替换）
- 重写文件 → `write_to_file`（自动覆盖）
- 新建文件 → `write_to_file`
- 删除文件 → `delete_file`（仅限确实要移除的文件）

---

## ⚠️ Shell 陷阱提醒

| 场景 | 危险 | 安全替代 |
|------|------|----------|
| 清理 out/ | `rd /s /q out` | `del /q out\*.js` 或 IDE 工具 |
| 清理 node_modules | `rd /s /q node_modules` | `npm ci`（会自动清理重装）|
| PowerShell 中用 cmd 语法 | 命令被错误解析 | 确认当前 Shell 类型再执行 |
| 路径含空格 | 未加引号导致截断 | 始终用引号包裹路径 |
| 变量拼接路径 | 变量为空则删根目录 | 先 echo 路径确认 |

---

## 🧠 核心原则

> **对破坏性操作保持极度偏执。**
> 
> 宁可多花 10 秒确认，也不要花 10 小时恢复。
> 
> 如果一个操作可能删除用户代码，就假设它**一定会**出错。
> 
> **能用 IDE 工具完成的事，绝不用终端命令。**

---

## 检查清单（执行危险操作前必须过一遍）

- [ ] 我确认了当前 Shell 是 PowerShell 还是 cmd？
- [ ] 我确认了目标路径是正确的（不是父目录）？
- [ ] 这个操作如果出错，最坏后果是什么？
- [ ] 有没有更安全的替代方案（IDE 工具）？
- [ ] 项目是否有 git 提交/远程备份可以恢复？
- [ ] 我是否可以用 `replace_in_file` 或 `write_to_file` 代替终端操作？
