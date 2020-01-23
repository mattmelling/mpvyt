with import <nixpkgs> {};
with pkgs.python37Packages;
buildPythonPackage {
  name = "mpvyt";
  src = ./.;
  version = "0.0.1";
  buildInputs = [
    beautifulsoup4
    requests
    lxml
  ];
}
