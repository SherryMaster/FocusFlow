[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName=FocusFlow
AppVersion=0.1.0
AppPublisher=Shaheer Ahmed
DefaultDirName={autopf}\FocusFlow
DefaultGroupName=FocusFlow
OutputDir=installer_output
OutputBaseFilename=FocusFlow-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Icons]
Name: "{autoprograms}\FocusFlow"; Filename: "{app}\main.exe"