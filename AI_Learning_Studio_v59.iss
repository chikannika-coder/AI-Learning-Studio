#define MyAppName "AI Learning Studio"
#define MyAppVersion "5.9"
#define MyAppExeName "AI_Learning_Studio_v59.exe"

[Setup]
AppId={{9B7635EA-8CB9-4BB2-B799-58F5A9050590}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\AI Learning Studio
DefaultGroupName=AI Learning Studio
OutputDir=installer
OutputBaseFilename=AI_Learning_Studio_v59_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=AI Learning Studio v5.9

[Files]
Source: "dist\AI_Learning_Studio_v59.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\AI Learning Studio"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\AI Learning Studio"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch AI Learning Studio"; Flags: nowait postinstall skipifsilent
