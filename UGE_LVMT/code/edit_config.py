import argparse
import os
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description="Simulation configuration updater")
    parser.add_argument("--log_dir", default="", help="Directory to save logs")
    parser.add_argument("--data_folder_directory", default="", help="Directory containing the data folder")
    parser.add_argument("--output_folder_directory", default="", help="Directory to store the output")
    parser.add_argument("--tmp_folder_directory", default="", help="Directory for temporary files")
    parser.add_argument("--sampling_rate", type=float, default=0.001, help="Sampling rate for the population")

    return parser.parse_args()

def update_config(
    config_directory: str,
    tmp_folder_directory: str,
    data_folder_directory: str,
    output_folder_directory: str,
    sampling_rate: float,
    processes: int = 4,
    hts: str = "entd",
    random_seed: int = 1234,
    java_memory: str = "48G",
    mode_choice: bool = False,
    regions: list = None,
    departments: list = None,
    gtfs_path: str = 'gtfs_npc',
    osm_path: str = 'osm_npc',
    ban_path: str = 'ban_npc',
    bdtopo_path: str = 'bdtopo_npc',
    osmosis_binary: str = '/app/osmosis/bin/osmosis'
):
    if regions is None:
        regions = []
    if departments is None:
        departments = ["59", "62"]

    # Create the configuration in the desired order
    updated_config = {
        'working_directory': tmp_folder_directory,
        'run': ['synthesis.output'],  # Add or update the 'run' key
        'config': {
            'processes': processes,
            'hts': hts,
            'sampling_rate': sampling_rate,
            'random_seed': random_seed,
            'data_path': data_folder_directory,
            'output_path': output_folder_directory,
            'java_memory': java_memory,
            'mode_choice': mode_choice,
            'regions': regions,
            'departments': departments,  # Use the departments list
            'gtfs_path': gtfs_path,
            'osm_path': osm_path,
            'ban_path': ban_path,
            'bdtopo_path': bdtopo_path,
            'osmosis_binary': osmosis_binary
        }
    }

    # Write the updated YAML content back to the file with the correct order
    with open(config_directory, 'w') as file:
        yaml.dump(updated_config, file, default_flow_style=False, sort_keys=False)

    print(f"Config file {config_directory} updated successfully.")

def main():
    args = parse_args()
    config_directory = os.path.join(str(args.log_dir), "equasim/config.yml")
    
    update_config(
        config_directory=config_directory,
        tmp_folder_directory=args.tmp_folder_directory,
        data_folder_directory=args.data_folder_directory,
        output_folder_directory=args.output_folder_directory,
        sampling_rate=args.sampling_rate
    )

if __name__ == "__main__":
    main()
