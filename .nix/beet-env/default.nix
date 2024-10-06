{ pkgs, python3 }:

(pkgs.poetry2nix.mkPoetryEnv {
  python = python3;
  projectDir = ./.;
  preferWheels = true;
  overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
  });
})
