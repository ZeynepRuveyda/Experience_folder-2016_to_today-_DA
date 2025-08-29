# 🚀 MLOps-Kubernetes-Kubeflow
## Nord-Pas-de-Calais automate the synthetic data creation project

Automate synthetic data creation and matsim simulation

![image](https://www.larousse.fr/encyclopedie/data/cartes/1309236-Nord-Pas-de-Calais.HD.jpg)

Source: www.larousse.fr

The MAP2050 research project, supported by ADEME, aims to develop new operational methods and tools to help design and monitor the execution of PCAETs, in partnership with the city of Dunkirk. As part of this project, the LVMT is in charge of lot 6 relating to simulations of changes in land use and the location of the population in relation to transport.
The aim of this project is to automate existing simulation algorithms using the necessary tools and to facilitate the user's work.

## The open-source data taken instruction from the links below:

https://github.com/eqasim-org/ile-de-france/blob/develop/docs/population.md

## 🗃️  Here is the structure of folder that you can use when you run your own code:

```bash
.
├── clone_test.yaml
├── code
│   ├── clone.py
│   ├── clone_try.py
│   ├── edit_config.py
│   ├── hello_world.yaml
│   ├── pipeline_demo.py
│   ├── pipeline_hello_world.py
│   ├── pipeline.py
│   ├── pvc_pipeline_hello_world.yaml
│   └── synpp.py
├── deployment.yaml
├── directory_structure.txt
├── Dockerfile
├── environment.txt
├── hello_world.yaml
├── npc
│   ├── data
│   │   ├── ban_npc
│   │   │   ├── adresses-59.csv.gz
│   │   │   └── adresses-62.csv.gz
│   │   ├── bdtopo_npc
│   │   │   ├── BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D059_2021-03-15.7z
│   │   │   └── BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D062_2021-03-15.7z
│   │   ├── bpe_2021
│   │   │   └── bpe21_ensemble_xy_csv.zip
│   │   ├── codes_2021
│   │   │   └── reference_IRIS_geo2021.zip
│   │   ├── entd_2008
│   │   │   ├── K_deploc.csv
│   │   │   ├── Q_individu.csv
│   │   │   ├── Q_ind_lieu_teg.csv
│   │   │   ├── Q_menage.csv
│   │   │   ├── Q_tcm_individu.csv
│   │   │   └── Q_tcm_menage_0.csv
│   │   ├── filosofi_2019
│   │   │   ├── indic-struct-distrib-revenu-2019-COMMUNES.zip
│   │   │   └── indic-struct-distrib-revenu-2019-SUPRA.zip
│   │   ├── gtfs_npc
│   │   │   ├── gtfs-20231115-161842-dkbus-annee-2024-2-.zip
│   │   │   ├── RHDF_GTFS_COM_62.zip
│   │   │   ├── RHDF_GTFS_COM_SCO_59_P1.zip
│   │   │   ├── RHDF_GTFS_COM_SCO_59_P2.zip
│   │   │   ├── RHDF_GTFS_COM_SCO_59_P3A.zip
│   │   │   ├── RHDF_GTFS_COM_SCO_59_P3B.zip
│   │   │   └── RHDF_GTFS_COM_SCO_59_P4.zip
│   │   ├── iris_2021
│   │   │   └── CONTOURS-IRIS_2-1__SHP__FRA_2021-01-01.7z
│   │   ├── osm_npc
│   │   │   └── nord-pas-de-calais-220101.osm.pbf
│   │   ├── projection_2021
│   │   │   └── 00_central.xlsx
│   │   ├── rp_2019
│   │   │   ├── base-ic-evol-struct-pop-2019.zip
│   │   │   ├── RP2019_INDCVI_csv.zip
│   │   │   ├── RP2019_MOBPRO_csv.zip
│   │   │   └── RP2019_MOBSCO_csv.zip
│   │   ├── sirene
│   │   │   ├── GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.zip
│   │   │   ├── StockEtablissement_utf8.zip
│   │   │   └── StockUniteLegale_utf8.zip
│   │   └── urban_type
│   │       └── UU2020_au_01-01-2023.zip
│   ├── output
│   └── tmp
├── pipeline_pyhton.yaml
├── pipeline_v_2.yaml
├── pipeline_v_3.yaml
├── pipeline_v_4.yaml
└── test_pv_pvc.yaml

18 directories, 52 files
```
## Version of the tools for local installation

**ubuntu** : 

Distributor ID: Ubuntu
Description:    Ubuntu 22.04.4 LTS
Release:        22.04
Codename:       jammy

**GitVersion**: "v1.27.13+k3s1”

**kubectl** : v1.27.13

**kubernetes**: v1.27.13

**Go version :** go1.21.9

**manifests** : v1.8.0

**kustomize**: v5.3.0


## Dependencies

**All the requirements needed for this projects is stored in the [requirement.txt](environment.txt) file.**

*to run it on your local computer follow the guideline with the link:*

https://www.notion.so/FULL-INSTALLATION-6f0387af141c414e81bcc85d4cde95b9


## Here are the Demos and enjoy with these  🤡

### 1) For kubeflow users
[Screencast from 06-14-2024 07:57:41 AM.webm](https://github.com/ZeynepRuveyda/MLOps-Kubernetes-Kubeflow/assets/72027409/f02ac4be-bb2e-47e5-befa-23f38789aee8)



### 2)For git clone & update the config.yaml

[automation_gitclone&configyaml.webm](https://github.com/ZeynepRuveyda/MLOps-Kubernetes-Kubeflow/assets/72027409/edcb8d56-ba19-4ae8-b5d6-90bcf75d3456)

# Reference Letter from Olivier Bonin
[Recommandation Ozel.pdf](https://github.com/user-attachments/files/19041457/Recommandation.Ozel.pdf)







