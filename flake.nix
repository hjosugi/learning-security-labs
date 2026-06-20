{
  description = "Development shell for local security learning labs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
            ];

            shellHook = ''
              echo "learning-security-labs dev shell"
              echo "Try: python3 projects/owasp-input-validation-lab/test_lab.py"
              echo "Try: python3 projects/access-control-lab/test_access_control.py"
            '';
          };
        });
    };
}
