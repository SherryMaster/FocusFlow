[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName=FocusFlow
AppVersion=1.0.0
AppPublisher=Shaheer Ahmed
DefaultDirName={autopf}\FocusFlow
DefaultGroupName=FocusFlow
OutputDir=installer_output
OutputBaseFilename=FocusFlow-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=assets/FocusFlow logo.ico

[Files]
Source: "dist\FocusFlow.exe"; DestDir: "{app}"

[Icons]
Name: "{autoprograms}\FocusFlow"; Filename: "{app}\FocusFlow.exe"