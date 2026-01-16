**Systems / Components**

- **HK01 Python System**: The primary project containing the elder-care Python code and ML integration.
  - Path: `d:\Github python\HK01(12.12.2025)(COMPETITION)`
  - Purpose: Camera/recognition pipeline, demos, and medication management helpers.

- **C++ First Project (CPP)**: A standalone C++ scaffold you placed at `D:\cpp_first_project`.
  - Path: `D:\cpp_first_project`
  - Purpose: Independent C++ experiment or component (Hello World scaffold with CMake and PowerShell build helper).

How to open both systems in VS Code:

- Option A (recommended): Open the workspace file `HK01_and_CPP.code-workspace` in VS Code (File → Open Workspace) — this will load both folders as separate roots.

- Option B: Add `D:\cpp_first_project` to the current workspace manually (File → Add Folder to Workspace...).

- Option C (if you prefer everything inside the repo): Copy `D:\cpp_first_project` into this workspace. Example PowerShell command:

```powershell
Copy-Item -Path "D:\cpp_first_project" -Destination "d:\Github python\HK01(12.12.2025)(COMPETITION)\cpp_first_project" -Recurse -Force
```

Notes:
- The multi-root workspace file references an absolute path outside the repository; you can keep using it locally or share it if collaborators have the same path layout.
- If you want, I can also create a top-level `Makefile` or a task to build the C++ project from within this workspace.
