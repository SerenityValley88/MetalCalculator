{ pkgs }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    streamlit
    # Add any other dependencies here like pandas, numpy, etc.
  ]);
in
  {
    deps = [
      pythonEnv
      pkgs.glibcLocales
    ];

    # Specify the run command for your Streamlit app
    shell = pkgs.bashInteractive;

    # You can also include additional setup tasks
    buildInputs = [ pythonEnv ];

    # Optionally, to expose ports
    environment.variables = {
      STREAMLIT_PORT = "5000";
    };
  }
