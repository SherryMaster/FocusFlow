[Setup]
AppName=FocusFlow
AppVersion=0.1.0
Publisher=Shaheer Ahmed
DefaultDirName={autopf}\FocusFlow
OutputDir=installer_output
OutputBaseFilename=FocusFlow-Setup

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Icons]
Name: "{autoprograms}\FocusFlow"; Filename: "{app}\main.exe"