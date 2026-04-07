; PharmaQMS Inno Setup Script
; Requires: Inno Setup 6.x (https://jrsoftware.org/isinfo.php)

#define MyAppName "PharmaQMS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PharmaQMS"
#define MyAppExeName "PharmaQMS.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=PharmaQMS-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加选项:"; Flags: checked

[Files]
; PyInstaller output directory
Source: "..\dist\PharmaQMS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Scripts
Source: "..\scripts\start.bat"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "..\scripts\stop.bat"; DestDir: "{app}\scripts"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\scripts\start.bat"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\停止 {#MyAppName}"; Filename: "{app}\scripts\stop.bat"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\scripts\start.bat"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\scripts\start.bat"; Description: "立即启动 PharmaQMS"; Flags: nowait postinstall skipifsilent shellexec

[UninstallRun]
Filename: "{app}\scripts\stop.bat"; Flags: runhidden
