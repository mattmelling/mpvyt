{
  description = "mpv youtube daemon";
  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlay ];
      };
    in {
      overlay = final: prev: {
        mpvyt = prev.callPackage ./default.nix { };
      };
    };
}
