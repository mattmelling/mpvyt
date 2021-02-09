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
      homeManagerModules = {
        mpvyt = { pkgs, config, lib, ... }: let
          cfg = config.services.mpvyt;
        in
          {
            options = with lib.types; {
              services.mpvyt = {
                enable = lib.mkEnableOption "mpvyt";
                playlist = lib.mkOption {
                  type = str;
                  description = "Where to store playlist file";
                };
              };
            };
            config = lib.mkIf cfg.enable {
              systemd.user.services.mpvyt = {
                Unit = {
                  Description = "mpvyt";
                };
                Install = {
                  WantedBy = [ "graphical-session.target" ];
                };
                Service = {
                  Type = "simple";
                  ExecStart = "${pkgs.mpvyt}/bin/mpvyt";
                  ExecStop = "${pkgs.killall}/bin/killall mpvyt";
                  Restart = "always";
                  Environment = "MPV_PLAYLIST_PATH=${cfg.playlist}";
                };
              };
            };
          };
      };
    };
}
