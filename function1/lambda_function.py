# from git.repo import Repo
# from git import RemoteProgress
import json
import os
import re
import subprocess
import tempfile

message_id_cache = {}
prefix_destination = os.getenv('prefix_destination') or ''
prefix_source = os.getenv('prefix_source')
repo_path = os.getenv('repo_path')
# repos to ignore
deny = {}
# if assigned repositories to allow

# just pigini

conversions = {"bitgdi-matrix1-kubix_lg_data-consumer": "fdh-matrix1-kubix_lg_data-consumer",
               "fdh-fdh-s3lab_ap-consumer": "bitgdi-fdh-s3lab_ap-consumer",
               "fdh-fdh-tracking-api": "bitgdi-fdh-tracking-api",
               "fdh-s3lab_garpe-ap-producer": "bitgdi-s3lab_garpe-ap-producer",
               "fdh-s3lab_tiger-ap-producer": "bitgdi-s3lab_tiger-ap-producer",
               "fdh-fdh-pigini_elastic_tracking-consumer": "bitgdi-fdh-pigini_elastic_tracking-consumer",
               "fdh-fdh-pigini_recovery_tracking-consumer": "bitgdi-fdh-pigini_recovery_tracking-consumer",
               "fdh-fdh-pigini_tracking-consumer": "bitgdi-fdh-pigini_tracking-consumer",
               "fdh-gps-s3lab_pigini_gpseof-consumer": "bitgdi-gps-s3lab_pigini_gpseof-consumer",
               "fdh-gps-s3lab_pigini_workorder_prop_fb-consumer": "bitgdi-gps-s3lab_pigini_workorder_prop_fb-consumer",
               "fdh-gps_pigini-trigger-producer": "bitgdi-pigini-gps-api",
               "fdh-gps_pigini_to_s3lab-simulatedhq-flow": "bitgdi-gps_pigini_to_s3lab-simulatedhq-flow",
               "fdh-gps_pigini_to_s3lab-suggestion_prod-flow": "bitgdi-gps_pigini_to_s3lab-suggestion_prod-flow",
               "fdh-gps_pigini_to_s3lab-suggestion_transf-flow": "bitgdi-gps_pigini_to_s3lab-suggestion_transf-flow",
               "fdh-gps_pigini_to_s3lab-workorder_ope-flow": "bitgdi-gps_pigini_to_s3lab-workorder_ope-flow",
               "fdh-gps_pigini_to_s3lab-workorder_prop-flow": "bitgdi-gps_pigini_to_s3lab-workorder_prop-flow",
               "fdh-jde_pigini-s3lab_pigini_data-consumer": "bitgdi-jde_pigini-s3lab_pigini_data-consumer",
               "fdh-jde_pigini_to_s3lab_pigini-anagrafiche-flow": "bitgdi-jde_pigini_to_s3lab_pigini-anagrafiche-flow",
               "fdh-jde_pigini_to_s3lab_pigini-cambi-flow": "bitgdi-jde_pigini_to_s3lab_pigini-cambi-flow",
               "fdh-mes_pigini-data-producer": "bitgdi-pigini-mes-api",
               "fdh-mes_pigini-s3lab_pigini_data-consumer": "bitgdi-mes_pigini-s3lab_pigini_data-consumer",
               "fdh-s3lab_pigini-ap-producer": "bitgdi-s3lab_pigini-ap-producer",
               "fdh-s3lab_pigini-data-producer": "bitgdi-s3lab_pigini-data-producer",
               "fdh-s3lab_pigini-gpstrigger-consumer": "bitgdi-s3lab_pigini-gpstrigger-consumer",
               "fdh-s3lab_pigini-mes_pigini_data-consumer": "bitgdi-s3lab_pigini-mes_pigini_data-consumer",
               "fdh-s3lab_pigini-trigger-producer": "bitgdi-pigini-s3lab-api",
               "fdh-s3lab_pigini_to_fdh_gps-cci-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cci-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cci_tgl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cci_tgl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-ccl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-ccl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cdb-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cdb-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cil-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cil-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cir-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cir-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cpr-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cpr-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cprtgl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cprtgl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-dbr-flow": "bitgdi-s3lab_pigini_to_fdh_gps-dbr-flow",
               "fdh-s3lab_pigini_to_fdh_gps-fab-flow": "bitgdi-s3lab_pigini_to_fdh_gps-fab-flow",
               "fdh-s3lab_pigini_to_fdh_gps-giaexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-giaexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-item-flow": "bitgdi-s3lab_pigini_to_fdh_gps-item-flow",
               "fdh-s3lab_pigini_to_fdh_gps-orfexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-orfexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-polexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-polexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-supplier-flow": "bitgdi-s3lab_pigini_to_fdh_gps-supplier-flow",
               "fdh-s3lab_pigini_to_fdh_gps-warehouse-flow": "bitgdi-s3lab_pigini_to_fdh_gps-warehouse-flow",
               "fdh-spc_ddc-s3lab_pigini_data-consumer": "bitgdi-spc_ddc-s3lab_pigini_data-consumer",
               "fdh-spc_to_s3lab_pigini-dcfo-flow": "bitgdi-spc_to_s3lab_pigini-dcfo-flow",
               "fdh-supplier_tag-s3lab_pigini_data-consumer": "bitgdi-supplier_tag-s3lab_pigini_data-consumer",
               "fdh-temera_rfid-s3lab_pigini_data-consumer": "bitgdi-rfid-s3lab_pigini_data-consumer",
               "fdh-digital-label-producer": "bitgdi-digital-label-producer",
               "fdh-fdh-digital-api": "bitgdi-digital-api",
               "fdh-dp_atlante_to_fdh-all-flow": "bitgdi-dp_atlante_to_fdh-all-flow",
               "fdh-enginenow_to_fdh-all-flow": "bitgdi-enginenow_to_fdh-all-flow",
               "fdh-fdh-hq_elastic_tracking-consumer": "bitgdi-fdh-hq_elastic_tracking-consumer",
               "fdh-fdh-hq_tracking-consumer": "bitgdi-fdh-hq_tracking-consumer",
               "fdh-gps_hq-trigger-producer": "bitgdi-hq-gps-api",
               "fdh-gps_hq_to_s3hq-suggestion_prod-flow": "bitgdi-gps_hq_to_s3hq-suggestion_prod-flow",
               "fdh-gps_hq_to_s3hq-workorder_prop-flow": "bitgdi-gps_hq_to_s3hq-workorder_prop-flow",
               "fdh-serpico_atlante_to_fdh-consumi-flow": "bitgdi-serpico_atlante_to_fdh-consumi-flow",
               "fdh-fdh-marbella_elastic_tracking-consumer": "bitgdi-fdh-marbella_elastic_tracking-consumer",
               "fdh-fdh-marbella_tracking-consumer": "bitgdi-fdh-marbella_tracking-consumer",
               "fdh-fdh-marbella_xtannery_data-consumer": "bitgdi-fdh-xtannery_marbella_data-consumer",
               "fdh-jde-marbella_xtannery_data-consumer": "bitgdi-jde-xtannery_marbella_data-consumer",
               "fdh-jde_marbella_to_xtannery_marbella-anagrafiche-flow": "bitgdi-jde_marbella_to_xtannery_marbella-anagrafiche-flow",
               "fdh-jde_marbella_to_xtannery_marbella-cambi-flow": "bitgdi-jde_marbella_to_xtannery_marbella-cambi-flow",
               "fdh-jde_marbella_to_xtannery_marbella-saldi-flow": "bitgdi-jde_marbella_to_xtannery_marbella-saldi-flow",
               "fdh-marbella-xtannery-api": "bitgdi-marbella-xtannery-api",
               "fdh-cim-verbali_nastri-producer": "bitgdi-cim-verbali_nastri-producer",
               "fdh-cim-verbali_pellami-producer": "bitgdi-cim-verbali_pellami-producer",
               "fdh-cim-verbali_tessuti-producer": "bitgdi-cim-verbali_tessuti-producer",
               "fdh-fdh-all_tracking-consumer": "bitgdi-fdh-all_tracking-consumer",
               "fdh-fdh-oozie_logs_elastic_tracking-flow": "bitgdi-fdh-oozie_logs_elastic_tracking-flow",
               "fdh-temera-data-producer": "bitgdi-rfid-api",
               "fdh-atlas-kubix-link-api": "bitgdi-kubix-api",
               "fdh-atlas-matrixone-api": "bitgdi-matrix1-api",
               "fdh-atlas-s400-api": "bitgdi-s400-api",
               "fdh-fdh-atlas_data-consumer": "bitgdi-fdh-atlas_data-consumer",
               "fdh-fdh-atlas_elastic_tracking-consumer": "bitgdi-fdh-atlas_elastic_tracking-consumer",
               "fdh-fdh-atlas_tracking-consumer": "bitgdi-fdh-atlas_tracking-consumer",
               "fdh-fdh-kubix-abilitazioni_stagionali-flow": "bitgdi-fdh_to_kubix-abilitazioni_stagionali-flow",
               "fdh-gms-matrixone-api": "bitgdi-gms-matrix1-api",
               "fdh-kubixlink-s3hq_data-consumer": "bitgdi-kubix-s3hq_data-consumer",
               "fdh-kubixlink-s400_data-consumer": "bitgdi-kubix-s400_data-consumer",
               "fdh-matrixone-s400_atlas_kubixlink_data-consumer": "bitgdi-matrix1-kubix_rm_data-consumer",
               "fdh-s400-atlas_kubixlink_data-consumer": "bitgdi-s400-kubix_rm_data-consumer",
               "fdh-spc-atlas_kubixlink_data-consumer": "bitgdi-plmsh-kubix_sh_data-consumer",
               "fdh-smc-atlas_kubixlink_data-consumer": "bitgdi-smc-kubix_rm_data-consumer",
               "fdh-kubixlink-matrixone_data-consumer": "bitgdi-kubix-matrix1_data-consumer",
               "fdh-matrix1-kubix_sh_data-consumer": "bitgdi-matrix1-kubix_sh_data-consumer",
               "fdh-plmsh-kubix_sh_data-consumer": "bitgdi-plmsh-kubix_sh_data-consumer",
               "fdh-s400-kubix_lg_data-consumer": "bitgdi-s400-kubix_lg_data-consumer",
               "fdh-s400-kubix_sh_data-consumer": "bitgdi-s400-kubix_sh_data-consumer",
               "fdh-dmh2-s3hq_data-consumer": "bitgdi-dmh2-s3hq_data-consumer",
               "fdh-fdh-gms_elastic_tracking-consumer": "bitgdi-fdh-gms_elastic_tracking-consumer",
               "fdh-fdh-gms_tracking-consumer": "bitgdi-fdh-gms_tracking-consumer",
               "fdh-s3hq-gms_matrixone_data-consumer": "bitgdi-s3hq-gms_matrix1_data-consumer",
               "fdh-tm_to_s3hq-scbs-flow": "bitgdi-tm_to_s3hq-scbs-flow",
               "fdh-fdh-sisc_sh_elastic_tracking-consumer": "bitgdi-fdh-spc_elastic_tracking-consumer",
               "fdh-fdh-sisc_sh_tracking-consumer": "bitgdi-fdh-spc_tracking-consumer",
               "fdh-sisc_sh-s3hq_data-consumer": "bitgdi-spc-s3hq_data-consumer",
               "fdh-sisc_sh_to_s3hq-ofan-flow": "bitgdi-spc_to_s3hq-ofan-flow",
               "fdh-spc_to_s3hq-dcou-flow": "bitgdi-spc_to_s3hq-dcou-flow",
               "fdh-tqapp_pac-sisc_pac-flow": "bitgdi-spc_to_tqapp_pac-flow",
               "fdh-aj_pigini-s3lab_sifa-cartellini-flow": "bitgdi-aj_pigini_to_s3lab_sifa-cartellini-flow",
               "fdh-aj_pigini-s3lab_sifa-ddt-flow": "bitgdi-aj_pigini_to_s3lab_sifa-ddt-flow",
               "fdh-aj_pigini-s3lab_sifa_data-consumer": "bitgdi-aj_pigini-s3lab_sifa_data-consumer",
               "fdh-boolebox-s3lab_sifa-workorderope-flow": "bitgdi-boolebox_to_s3lab_sifa-workorderope-flow",
               "fdh-fdh-sifa_elastic_tracking-consumer": "bitgdi-fdh-sifa_elastic_tracking-consumer",
               "fdh-fdh-sifa_recovery_tracking-consumer": "bitgdi-fdh-sifa_recovery_tracking-consumer",
               "fdh-fdh-sifa_tracking-consumer": "bitgdi-fdh-sifa_tracking-consumer",
               "fdh-fdhgir-mes_v1_sifa_data-consumer": "bitgdi-fdh_gir-mes_v1_sifa_data-consumer",
               "fdh-fdhmd-s3lab_sifa_data-consumer": "bitgdi-fdh_md-s3lab_sifa_data-consumer",
               "fdh-mes_sifa-data-producer": "bitgdi-sifa-mes-api",
               "fdh-mes_sifa-s3lab_sifa_data-consumer": "bitgdi-mes_sifa-s3lab_sifa_data-consumer",
               "fdh-mes_v1_sifa-data-producer": "bitgdi-sifa-mes-v1-api",
               "fdh-mes_v1_sifa-s3lab_sifa_data-consumer": "bitgdi-mes_v1_sifa-s3lab_sifa_data-consumer",
               "fdh-s3lab_sifa-data-producer": "bitgdi-s3lab_sifa-data-producer",
               "fdh-s3lab_sifa-mes_sifa_data-consumer": "bitgdi-s3lab_sifa-mes_sifa_data-consumer",
               "fdh-s3lab_sifa-mes_v1_sifa_data-consumer": "bitgdi-s3lab_sifa-mes_v1_sifa_data-consumer",
               "fdh-fdh-dwh_elastic_tracking-consumer": "bitgdi-fdh-dwh_elastic_tracking-consumer",
               "fdh-fdh-dwh_tracking-consumer": "bitgdi-fdh-dwh_tracking-consumer",
               "fdh-s3hq_costi_to_dwh_costi-reporting-flow": "bitgdi-s3hq_costi_to_dwh_costi-reporting-flow",
               "fdh-s3hq_fatti_to_dwh_fatti-reporting-flow": "bitgdi-s3hq_fatti_to_dwh_fatti-reporting-flow",
               "fdh-s3hq_fatture_to_dwh_fatture-reporting-flow": "bitgdi-s3hq_fatture_to_dwh_fatture-reporting-flow",
               "fdh-s3hq_lookup_to_dwh_lookup-reporting-flow": "bitgdi-s3hq_lookup_to_dwh_lookup-reporting-flow",
               "fdh-s3lab_garpe_costi_to_dwh_costi-reporting-flow": "bitgdi-s3lab_garpe_costi_to_dwh_costi-reporting-flow",
               "fdh-s3lab_garpe_fatti_to_dwh_fatti-reporting-flow": "bitgdi-s3lab_garpe_fatti_to_dwh_fatti-reporting-flow",
               "fdh-s3lab_garpe_fatture_to_dwh_fatture-reporting-flow": "bitgdi-s3lab_garpe_fatture_to_dwh_fatture-reporting-flow",
               "fdh-s3lab_garpe_lookup_to_dwh_lookup-reporting-flow": "bitgdi-s3lab_garpe_lookup_to_dwh_lookup-reporting-flow",
               "fdh-s3lab_gg_lookup_to_dwh_lookup-reporting-flow": "bitgdi-s3lab_gg_lookup_to_dwh_lookup-reporting-flow",
               "fdh-s3lab_pigini_costi_to_dwh_costi-reporting-flow": "bitgdi-s3lab_pigini_costi_to_dwh_costi-reporting-flow",
               "fdh-s3lab_pigini_fatti_to_dwh_fatti-reporting-flow": "bitgdi-s3lab_pigini_fatti_to_dwh_fatti-reporting-flow",
               "fdh-s3lab_pigini_fatture_to_dwh_fatture-reporting-flow": "bitgdi-s3lab_pigini_fatture_to_dwh_fatture-reporting-flow",
               "fdh-s3lab_pigini_lookup_to_dwh_lookup-reporting-flow": "bitgdi-s3lab_pigini_lookup_to_dwh_lookup-reporting-flow",
               "fdh-s3lab_tiger_costi_to_dwh_costi-reporting-flow": "bitgdi-s3lab_tiger_costi_to_dwh_costi-reporting-flow",
               "fdh-s3lab_tiger_fatti_to_dwh_fatti-reporting-flow": "bitgdi-s3lab_tiger_fatti_to_dwh_fatti-reporting-flow",
               "fdh-s3lab_tiger_fatture_to_dwh_fatture-reporting-flow": "bitgdi-s3lab_tiger_fatture_to_dwh_fatture-reporting-flow",
               "fdh-s3lab_tiger_lookup_to_dwh_lookup-reporting-flow": "bitgdi-s3lab_tiger_lookup_to_dwh_lookup-reporting-flow",
               "fdh-fdh-garpe_elastic_tracking-consumer": "bitgdi-fdh-garpe_elastic_tracking-consumer",
               "fdh-fdh-garpe_recovery_tracking-consumer": "bitgdi-fdh-garpe_recovery_tracking-consumer",
               "fdh-fdh-garpe_tracking-consumer": "bitgdi-fdh-garpe_tracking-consumer",
               "fdh-fdh_garpe-updated_wo-producer": "bitgdi-fdh_garpe-updated_wo-producer",
               "fdh-fdh_norm_wop-fdh_garpe_updated_wo-consumer": "bitgdi-fdh_norm_wop-fdh_garpe_updated_wo-consumer",
               "fdh-gps-s3lab_garpe_gpseof-consumer": "bitgdi-gps-s3lab_garpe_gpseof-consumer",
               "fdh-gps_garpe-mes_garpe_data-consumer": "bitgdi-gps_garpe-mes_garpe_data-consumer",
               "fdh-gps_garpe-trigger-producer": "bitgdi-garpe-gps-api",
               "fdh-gps_garpe-workorder_ope-producer": "bitgdi-gps_garpe-workorder_ope-producer",
               "fdh-gps_garpe-workorder_prop-producer": "bitgdi-gps_garpe-workorder_prop-producer",
               "fdh-gps_garpe_to_mes-wolot-flow": "bitgdi-gps_garpe_to_mes-wolot-flow",
               "fdh-gps_garpe_to_rfid-wolot-flow": "bitgdi-gps_garpe_to_rfid-wolot-flow",
               "fdh-mes_garpe-data-producer": "bitgdi-garpe-mes-api",
               "fdh-mes_garpe-gps_workorder_ope-consumer": "bitgdi-mes_garpe-gps_workorder_ope-consumer",
               "fdh-mes_garpe-s3lab_garpe_data-consumer": "bitgdi-mes_garpe-s3lab_garpe_data-consumer",
               "fdh-s3lab_garpe-ap-producer": "bitgdi-s3lab_garpe-ap-producer",
               "fdh-s3lab_garpe-data-producer": "bitgdi-s3lab_garpe-data-producer",
               "fdh-s3lab_garpe-gps_workorder_ope-consumer": "bitgdi-s3lab_garpe-gps_workorder_ope-consumer",
               "fdh-s3lab_garpe-gps_workorder_prop-consumer": "bitgdi-s3lab_garpe-gps_workorder_prop-consumer",
               "fdh-s3lab_garpe-gpstrigger-producer": "bitgdi-garpe-s3lab-api",
               "fdh-s3lab_garpe-mes_garpe_data-consumer": "bitgdi-s3lab_garpe-mes_garpe_data-consumer",
               "fdh-s3lab_garpe_to_fdh_gps-cci-flow": "bitgdi-s3lab_garpe_to_fdh_gps-cci-flow",
               "fdh-s3lab_garpe_to_fdh_gps-ccl-flow": "bitgdi-s3lab_garpe_to_fdh_gps-ccl-flow",
               "fdh-s3lab_garpe_to_fdh_gps-cdb-flow": "bitgdi-s3lab_garpe_to_fdh_gps-cdb-flow",
               "fdh-s3lab_garpe_to_fdh_gps-cpr-flow": "bitgdi-s3lab_garpe_to_fdh_gps-cpr-flow",
               "fdh-s3lab_garpe_to_fdh_gps-cprtgl-flow": "bitgdi-s3lab_garpe_to_fdh_gps-cprtgl-flow",
               "fdh-s3lab_garpe_to_fdh_gps-giaexp-flow": "bitgdi-s3lab_garpe_to_fdh_gps-giaexp-flow",
               "fdh-s3lab_garpe_to_fdh_gps-item-flow": "bitgdi-s3lab_garpe_to_fdh_gps-item-flow",
               "fdh-s3lab_garpe_to_fdh_gps-orfexp-flow": "bitgdi-s3lab_garpe_to_fdh_gps-orfexp-flow",
               "fdh-s3lab_garpe_to_fdh_gps-polexp-flow": "bitgdi-s3lab_garpe_to_fdh_gps-polexp-flow",
               "fdh-s3lab_garpe_to_fdh_gps-supplier-flow": "bitgdi-s3lab_garpe_to_fdh_gps-supplier-flow",
               "fdh-s3lab_garpe_to_jde-fa-flow": "bitgdi-s3lab_garpe_to_jde-fa-flow",
               "fdh-s3lab_garpe_to_jde-fp-flow": "bitgdi-s3lab_garpe_to_jde-fp-flow",
               "fdh-sisc_d2-s3lab_garpe_data-consumer": "bitgdi-sisc_d2-s3lab_garpe_data-consumer",
               "fdh-sisc_ddc-s3lab_garpe_data-consumer": "bitgdi-sisc_ddc-s3lab_garpe_data-consumer",
               "fdh-fdh-tiger_elastic_tracking-consumer": "bitgdi-fdh-tiger_elastic_tracking-consumer",
               "fdh-fdh-tiger_recovery_tracking-consumer": "bitgdi-fdh-tiger_recovery_tracking-consumer",
               "fdh-fdh-tiger_tracking-consumer": "bitgdi-fdh-tiger_tracking-consumer",
               "fdh-gps-s3lab_tiger_gpseof-consumer": "bitgdi-gps-s3lab_tiger_gpseof-consumer",
               "fdh-gps-s3lab_tiger_workorder_prop_fb-consumer": "bitgdi-gps-s3lab_tiger_workorder_prop_fb-consumer",
               "fdh-gps_tiger-trigger-producer": "bitgdi-tiger-gps-api",
               "fdh-gps_tiger_to_s3lab-simulatedhq-flow": "bitgdi-gps_tiger_to_s3lab-simulatedhq-flow",
               "fdh-gps_tiger_to_s3lab-suggestion_prod-flow": "bitgdi-gps_tiger_to_s3lab-suggestion_prod-flow",
               "fdh-gps_tiger_to_s3lab-suggestion_transf-flow": "bitgdi-gps_tiger_to_s3lab-suggestion_transf-flow",
               "fdh-gps_tiger_to_s3lab-workorder_ope-flow": "bitgdi-gps_tiger_to_s3lab-workorder_ope-flow",
               "fdh-gps_tiger_to_s3lab-workorder_prop-flow": "bitgdi-gps_tiger_to_s3lab-workorder_prop-flow",
               "fdh-jde_tiger-s3lab_tiger_data-consumer": "bitgdi-jde_tiger-s3lab_tiger_data-consumer",
               "fdh-jde_tiger_to_s3lab_tiger-anagrafiche-flow": "bitgdi-jde_tiger_to_s3lab_tiger-anagrafiche-flow",
               "fdh-jde_tiger_to_s3lab_tiger-cambi-flow": "bitgdi-jde_tiger_to_s3lab_tiger-cambi-flow",
               "fdh-mes_tiger-data-producer": "bitgdi-tiger-mes-api",
               "fdh-mes_tiger-s3lab_tiger_data-consumer": "bitgdi-mes_tiger-s3lab_tiger_data-consumer",
               "fdh-s3lab_tiger-ap-producer": "bitgdi-s3lab_tiger-ap-producer",
               "fdh-s3lab_tiger-data-producer": "bitgdi-s3lab_tiger-data-producer",
               "fdh-s3lab_tiger-gpstrigger-consumer": "bitgdi-s3lab_tiger-gpstrigger-consumer",
               "fdh-s3lab_tiger-mes_tiger_data-consumer": "bitgdi-s3lab_tiger-mes_tiger_data-consumer",
               "fdh-s3lab_tiger-trigger-producer": "bitgdi-tiger-s3lab-api",
               "fdh-s3lab_tiger_to_fdh_gps-cci-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cci-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cci_tgl-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cci_tgl-flow",
               "fdh-s3lab_tiger_to_fdh_gps-ccl-flow": "bitgdi-s3lab_tiger_to_fdh_gps-ccl-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cdb-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cdb-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cil-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cil-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cir-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cir-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cpr-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cpr-flow",
               "fdh-s3lab_tiger_to_fdh_gps-cprtgl-flow": "bitgdi-s3lab_tiger_to_fdh_gps-cprtgl-flow",
               "fdh-s3lab_tiger_to_fdh_gps-dbr-flow": "bitgdi-s3lab_tiger_to_fdh_gps-dbr-flow",
               "fdh-s3lab_tiger_to_fdh_gps-fab-flow": "bitgdi-s3lab_tiger_to_fdh_gps-fab-flow",
               "fdh-s3lab_tiger_to_fdh_gps-giaexp-flow": "bitgdi-s3lab_tiger_to_fdh_gps-giaexp-flow",
               "fdh-s3lab_tiger_to_fdh_gps-item-flow": "bitgdi-s3lab_tiger_to_fdh_gps-item-flow",
               "fdh-s3lab_tiger_to_fdh_gps-orfexp-flow": "bitgdi-s3lab_tiger_to_fdh_gps-orfexp-flow",
               "fdh-s3lab_tiger_to_fdh_gps-polexp-flow": "bitgdi-s3lab_tiger_to_fdh_gps-polexp-flow",
               "fdh-s3lab_tiger_to_fdh_gps-supplier-flow": "bitgdi-s3lab_tiger_to_fdh_gps-supplier-flow",
               "fdh-s3lab_tiger_to_fdh_gps-warehouse-flow": "bitgdi-s3lab_tiger_to_fdh_gps-warehouse-flow",
               "fdh-spc_ddc-s3lab_tiger_data-consumer": "bitgdi-spc_ddc-s3lab_tiger_data-consumer",
               "fdh-spc_to_s3lab_tiger-dcfo-flow": "bitgdi-spc_to_s3lab_tiger-dcfo-flow",
               "fdh-supplier_tag-s3lab_tiger_data-consumer": "bitgdi-supplier_tag-s3lab_tiger_data-consumer",
               "fdh-temera_rfid-s3lab_tiger_data-consumer": "bitgdi-rfid-s3lab_tiger_data-consumer",
               "fdh-changelog-s3hq_data-consumer": "bitgdi-fdh_changelog-s3hq_data-consumer",
               "fdh-eas-docin-producer": "bitgdi-eas-docin-producer",
               "fdh-eas-giacenza-producer": "bitgdi-eas-giacenza-producer",
               "fdh-eas-movimenti-producer": "bitgdi-eas-movimenti-producer",
               "fdh-eas-ordini-producer": "bitgdi-eas-ordini-producer",
               "fdh-eas-s3hq_wms_data-consumer": "bitgdi-eas-s3hq_data-consumer",
               "fdh-eas-spedizioni-producer": "bitgdi-eas-spedizioni-producer",
               "fdh-fdh-s3hq_wms_tracking-consumer": "bitgdi-fdh-wms_tracking-consumer",
               "fdh-fdh-wms_elastic_tracking-consumer": "bitgdi-fdh-wms_elastic_tracking-consumer",
               "fdh-fdh-wms_recovery_tracking-consumer": "bitgdi-fdh-wms_recovery_tracking-consumer",
               "fdh-s3hq_wms-data-producer": "bitgdi-s3hq-data-producer",
               "fdh-s3hq_wms-eas_docin-consumer": "bitgdi-s3hq-eas_docin-consumer",
               "fdh-s3hq_wms-eas_giacenza-consumer": "bitgdi-s3hq-eas_giacenza-consumer",
               "fdh-s3hq_wms-eas_movimenti-consumer": "bitgdi-s3hq-eas_movimenti-consumer",
               "fdh-s3hq_wms-eas_ordini-consumer": "bitgdi-s3hq-eas_ordini-consumer",
               "fdh-s3hq_wms-eas_spedizioni-consumer": "bitgdi-s3hq-eas_spedizioni-consumer",
               "fdh-tms-s3hq_wms_data-consumer": "bitgdi-tms-s3hq_data-consumer",
               "fdh-tms_to_s3hq-ddt-flow": "bitgdi-tms_to_s3hq-ddt-flow",
               "fdh-mes_garpe-temera_data-consumer": "bitgdi-mes_garpe-rfid_data-consumer",
               "fdh-gecook-s3hq_data-consumer": "bitgdi-gecook-s3hq_data-consumer",
               "fdh-matrix1-kubix_lg_data-consumer": "bitgdi-matrix1-kubix_lg_data-consumer",
               "fdh-mes_garpe-cim_verbali_concerie-consumer": "bitgdi-mes_garpe-cim_verbali_concerie-consumer",
               "fdh-fdh-sap_globe_data-consumer": "bitgdi-fdh-sap_globe_data-consumer",
               "fdh-fdh-all_elastic_tracking-consumer": "bitgdi-fdh-all_elastic_tracking-consumer",
               "fdh-atlas-plab-api": "bitgdi-plab-api",
               "bitgdi-idwh_ares_phoenix": "fdh-idwh_ares_phoenix",
               "fdh-edac-api": "bitgdi-edac-api"}


allow = [x for x in conversions.keys()]


def handler(event, context):
    print("incoming event:" + json.dumps(event))
    common = event['Records'][0]['Sns']
    message_id = common['MessageId']
    # avoid processing duplicated request (sns can send duplicated
    # https://cloudonaut.io/your-lambda-function-might-execute-twice-deal-with-it/)
    # global variables in python are maintained between invocations if
    # lambda is not recreated by AWS (so it's not accurately unique)
    if message_id_cache.get(message_id, None):
        print("event with MessageId: {} already processed".format(message_id))
        return
    else:
        message_id_cache[message_id] = '1'
    m = json.loads(common['Message'])
    repo_source = m["detail"]["repositoryName"]
    if repo_source in deny:
        print("{} is present in ignore list, skipping".format(repo_source))
        return event
    if allow is None:
        print("allow list is empty, continuing")
    elif repo_source in allow:
        print("{} is present in allow list, continuing".format(repo_source))
    else:
        print("{} is not on allow list, exiting".format(repo_source))
        return event
    # check if special conversion exists
    repo_destination = None
    repo_converted = conversions.get(repo_source, repo_source)
    if repo_converted != repo_source:
        print("converted from dict {}->{}".format(repo_source, repo_converted))
        repo_destination = repo_converted
    else:
        repo_destination = re.sub(re.compile("^{}".format(prefix_source)),
                                  prefix_destination, repo_source)
        print("converted from sub {}->{}".format(repo_source,
                                                 repo_destination))

    with tempfile.TemporaryDirectory() as clone_dir:
        os.environ['HOME'] = "/tmp"
        os.environ['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -i $HOME/.ssh/id_rsa'
        print(os.getenv('HOME'))
        print(os.getenv('GIT_SSH_COMMAND'))
        clone = """
        mkdir -p $HOME/.ssh;
        cp id_rsa $HOME/.ssh;
        chmod 600 $HOME/.ssh/id_rsa;
        git clone --mirror {source} {clone_dir};
        cd {clone_dir};
        git remote add dest {destination};
        git push dest --mirror
        """.format(source="{}/{}".format(repo_path, repo_source),
                   clone_dir=clone_dir,
                   destination="{}/{}".format(repo_path, repo_destination),
                   path="/tmp/usr/bin")
        print(clone)
        ret = subprocess.run(clone,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        print(ret.stdout.decode('utf-8'))
        if ret.returncode > 0:
            print("[ERROR] {clone} gave {result} with {error}".format(
                clone=clone,
                result=ret.stdout.decode('utf-8'),
                error=ret.stderr.decode('utf-8')).replace("\n", "\\n"))
    return event
