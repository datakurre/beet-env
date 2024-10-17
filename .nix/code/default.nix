{
  vscode-with-extensions,
  vscode-extensions,
  vscode-marketplace,
  vscode-utils,
  vscodium,
  ruff,
  lib,
  enableVim ? false,
}:

let
  mecha-language-server = vscode-utils.buildVscodeMarketplaceExtension rec {
    mktplcRef = {
      name = "mecha-language-server";
      version = "0.1.0";
      publisher = "TheNuclearNexus";
    };
    vsix = ./mecha-language-server-0.1.0.zip;
  };

in
vscode-with-extensions.override {
  vscode = vscodium;
  vscodeExtensions = [
    mecha-language-server
    vscode-extensions.bbenoist.nix
    vscode-extensions.ms-pyright.pyright
    vscode-extensions.ms-python.python
    vscode-extensions.ms-vscode.makefile-tools
    (vscode-marketplace.charliermarsh.ruff.overrideAttrs (old: {
      postInstall = ''
        rm -f $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
        ln -s ${ruff}/bin/ruff $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
      '';
    }))
    vscode-marketplace.minecraftcommands.syntax-mcfunction
  ] ++ lib.optionals enableVim [ vscode-extensions.vscodevim.vim ];
}