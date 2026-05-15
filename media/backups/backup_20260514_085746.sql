--
-- PostgreSQL database dump
--

\restrict A6mucbCYoRc1fMwXeGccmOkxP6nr1fUNByQkem0AtSaDN1IcU403Jk20LAQSy69

-- Dumped from database version 14.20 (Homebrew)
-- Dumped by pg_dump version 16.10 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.reports_report DROP CONSTRAINT IF EXISTS reports_report_created_by_id_e9adac24_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_userrole DROP CONSTRAINT IF EXISTS crm_userrole_user_id_e281baa8_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_userrole DROP CONSTRAINT IF EXISTS crm_userrole_role_id_764fcdba_fk_crm_role_id;
ALTER TABLE IF EXISTS ONLY public.crm_user_user_permissions DROP CONSTRAINT IF EXISTS crm_user_user_permissions_user_id_047208b5_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_user_user_permissions DROP CONSTRAINT IF EXISTS crm_user_user_permis_permission_id_0f701f96_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.crm_user_groups DROP CONSTRAINT IF EXISTS crm_user_groups_user_id_5847c7a0_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_user_groups DROP CONSTRAINT IF EXISTS crm_user_groups_group_id_93d3047c_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.crm_techcardvariant DROP CONSTRAINT IF EXISTS crm_techcardvariant_tech_card_id_43f7c6d6_fk_crm_techcard_id;
ALTER TABLE IF EXISTS ONLY public.crm_techcardcomponent DROP CONSTRAINT IF EXISTS crm_techcardcomponent_tech_card_id_623c4128_fk_crm_techcard_id;
ALTER TABLE IF EXISTS ONLY public.crm_techcardcomponent DROP CONSTRAINT IF EXISTS crm_techcardcomponen_ingredient_id_4ce9ea00_fk_crm_ingre;
ALTER TABLE IF EXISTS ONLY public.crm_techcard DROP CONSTRAINT IF EXISTS crm_techcard_dish_id_277af818_fk_crm_dish_id;
ALTER TABLE IF EXISTS ONLY public.crm_techcard DROP CONSTRAINT IF EXISTS crm_techcard_approved_by_id_32ef922d_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_routestop DROP CONSTRAINT IF EXISTS crm_routestop_route_id_38bf345b_fk_crm_route_id;
ALTER TABLE IF EXISTS ONLY public.crm_routestop DROP CONSTRAINT IF EXISTS crm_routestop_proof_uploaded_by_id_13f26b97_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_routestop DROP CONSTRAINT IF EXISTS crm_routestop_proof_reviewed_by_id_27311351_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_routestop DROP CONSTRAINT IF EXISTS crm_routestop_delivery_id_c0c90c7b_fk_crm_delivery_id;
ALTER TABLE IF EXISTS ONLY public.crm_route DROP CONSTRAINT IF EXISTS crm_route_logistician_id_a5ae8d10_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_productionreservation DROP CONSTRAINT IF EXISTS crm_productionreservation_order_id_4efb72f7_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_pickingsession DROP CONSTRAINT IF EXISTS crm_pickingsession_picker_id_ee342393_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_pickingsession DROP CONSTRAINT IF EXISTS crm_pickingsession_order_id_3b52eab3_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_orderitem DROP CONSTRAINT IF EXISTS crm_orderitem_order_id_7ec9f773_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_orderitem DROP CONSTRAINT IF EXISTS crm_orderitem_ingredient_id_2185a1eb_fk_crm_ingredient_id;
ALTER TABLE IF EXISTS ONLY public.crm_orderitem DROP CONSTRAINT IF EXISTS crm_orderitem_dish_id_e3114b2a_fk_crm_dish_id;
ALTER TABLE IF EXISTS ONLY public.crm_orderitem DROP CONSTRAINT IF EXISTS crm_orderitem_custom_tech_card_id_5e4ea50e_fk_crm_techcard_id;
ALTER TABLE IF EXISTS ONLY public.crm_order DROP CONSTRAINT IF EXISTS crm_order_manager_id_039a402f_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_order DROP CONSTRAINT IF EXISTS crm_order_client_id_8ed70023_fk_crm_client_id;
ALTER TABLE IF EXISTS ONLY public.crm_logisticianprofile DROP CONSTRAINT IF EXISTS crm_logisticianprofile_user_id_734435f2_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_interaction DROP CONSTRAINT IF EXISTS crm_interaction_manager_id_24afb2b9_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_interaction DROP CONSTRAINT IF EXISTS crm_interaction_client_id_e63a8170_fk_crm_client_id;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientstock DROP CONSTRAINT IF EXISTS crm_ingredientstock_ingredient_id_8f0c8b74_fk_crm_ingredient_id;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientreservation DROP CONSTRAINT IF EXISTS crm_ingredientreservation_order_id_17138f75_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientreservation DROP CONSTRAINT IF EXISTS crm_ingredientreserv_ingredient_id_a8564254_fk_crm_ingre;
ALTER TABLE IF EXISTS ONLY public.crm_equipmentreservation DROP CONSTRAINT IF EXISTS crm_equipmentreservation_order_id_e9f68c20_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_equipmentreservation DROP CONSTRAINT IF EXISTS crm_equipmentreserva_equipment_id_01460725_fk_crm_equip;
ALTER TABLE IF EXISTS ONLY public.crm_dishequipmentrequirement DROP CONSTRAINT IF EXISTS crm_dishequipmentrequirement_dish_id_d09c1cdf_fk_crm_dish_id;
ALTER TABLE IF EXISTS ONLY public.crm_dishequipmentrequirement DROP CONSTRAINT IF EXISTS crm_dishequipmentreq_equipment_id_c03741cd_fk_crm_equip;
ALTER TABLE IF EXISTS ONLY public.crm_dish DROP CONSTRAINT IF EXISTS crm_dish_created_by_id_1ec5aa20_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_delivery DROP CONSTRAINT IF EXISTS crm_delivery_route_id_7a215b73_fk_crm_route_id;
ALTER TABLE IF EXISTS ONLY public.crm_delivery DROP CONSTRAINT IF EXISTS crm_delivery_order_id_88ce6731_fk_crm_order_id;
ALTER TABLE IF EXISTS ONLY public.crm_delivery DROP CONSTRAINT IF EXISTS crm_delivery_courier_id_fa676b65_fk_crm_courier_id;
ALTER TABLE IF EXISTS ONLY public.crm_courierassignment DROP CONSTRAINT IF EXISTS crm_courierassignment_route_id_40d05eac_fk_crm_route_id;
ALTER TABLE IF EXISTS ONLY public.crm_courierassignment DROP CONSTRAINT IF EXISTS crm_courierassignment_courier_id_d66fb584_fk_crm_courier_id;
ALTER TABLE IF EXISTS ONLY public.crm_courier DROP CONSTRAINT IF EXISTS crm_courier_user_id_2f7f2458_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_clientstagehistory DROP CONSTRAINT IF EXISTS crm_clientstagehistory_client_id_926d0169_fk_crm_client_id;
ALTER TABLE IF EXISTS ONLY public.crm_clientstagehistory DROP CONSTRAINT IF EXISTS crm_clientstagehistory_changed_by_id_84f6d086_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_clientstagehistory DROP CONSTRAINT IF EXISTS crm_clientstagehisto_stage_id_04e1997a_fk_crm_coope;
ALTER TABLE IF EXISTS ONLY public.crm_clientcontact DROP CONSTRAINT IF EXISTS crm_clientcontact_client_id_b44e105e_fk_crm_client_id;
ALTER TABLE IF EXISTS ONLY public.crm_clientallowedtechcard DROP CONSTRAINT IF EXISTS crm_clientallowedtechcard_client_id_a202bbc1_fk_crm_client_id;
ALTER TABLE IF EXISTS ONLY public.crm_clientallowedtechcard DROP CONSTRAINT IF EXISTS crm_clientallowedtec_tech_card_id_4956fc6d_fk_crm_techc;
ALTER TABLE IF EXISTS ONLY public.crm_client DROP CONSTRAINT IF EXISTS crm_client_responsible_manager_id_7081e9b4_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.crm_client DROP CONSTRAINT IF EXISTS crm_client_current_stage_id_e8a55701_fk_crm_cooperationstage_id;
ALTER TABLE IF EXISTS ONLY public.crm_auditlog DROP CONSTRAINT IF EXISTS crm_auditlog_actor_id_4382924f_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.communications_entitycomment DROP CONSTRAINT IF EXISTS communications_entitycomment_author_id_b58bd8f7_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.communications_entitycomment DROP CONSTRAINT IF EXISTS communications_entit_content_type_id_71d2a881_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.communications_directmessage DROP CONSTRAINT IF EXISTS communications_directmessage_sender_id_5355d0f2_fk_crm_user_id;
ALTER TABLE IF EXISTS ONLY public.communications_directmessage DROP CONSTRAINT IF EXISTS communications_direc_recipient_id_267e91bf_fk_crm_user_;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.admin_panel_backup DROP CONSTRAINT IF EXISTS admin_panel_backup_created_by_id_f9e87668_fk_crm_user_id;
DROP TRIGGER IF EXISTS trg_crm_orderitem_total_recalc ON public.crm_orderitem;
DROP TRIGGER IF EXISTS trg_crm_orderitem_prepare ON public.crm_orderitem;
DROP TRIGGER IF EXISTS trg_crm_order_validate_delivery_date ON public.crm_order;
DROP TRIGGER IF EXISTS trg_crm_ingredientreservation_check ON public.crm_ingredientreservation;
DROP INDEX IF EXISTS public.reports_report_created_by_id_e9adac24;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.crm_userrole_user_id_e281baa8;
DROP INDEX IF EXISTS public.crm_userrole_role_id_764fcdba;
DROP INDEX IF EXISTS public.crm_user_username_1ca997f7_like;
DROP INDEX IF EXISTS public.crm_user_user_permissions_user_id_047208b5;
DROP INDEX IF EXISTS public.crm_user_user_permissions_permission_id_0f701f96;
DROP INDEX IF EXISTS public.crm_user_groups_user_id_5847c7a0;
DROP INDEX IF EXISTS public.crm_user_groups_group_id_93d3047c;
DROP INDEX IF EXISTS public.crm_user_email_3827a8fd_like;
DROP INDEX IF EXISTS public.crm_techcardvariant_tech_card_id_43f7c6d6;
DROP INDEX IF EXISTS public.crm_techcardcomponent_tech_card_id_623c4128;
DROP INDEX IF EXISTS public.crm_techcardcomponent_ingredient_id_4ce9ea00;
DROP INDEX IF EXISTS public.crm_techcard_dish_id_277af818;
DROP INDEX IF EXISTS public.crm_techcard_approved_by_id_32ef922d;
DROP INDEX IF EXISTS public.crm_routestop_route_id_38bf345b;
DROP INDEX IF EXISTS public.crm_routestop_proof_uploaded_by_id_13f26b97;
DROP INDEX IF EXISTS public.crm_routestop_proof_reviewed_by_id_27311351;
DROP INDEX IF EXISTS public.crm_routestop_delivery_id_c0c90c7b;
DROP INDEX IF EXISTS public.crm_route_logistician_id_a5ae8d10;
DROP INDEX IF EXISTS public.crm_role_name_9490777a_like;
DROP INDEX IF EXISTS public.crm_productionreservation_order_id_4efb72f7;
DROP INDEX IF EXISTS public.crm_pickingsession_picker_id_ee342393;
DROP INDEX IF EXISTS public.crm_orderitem_order_id_7ec9f773;
DROP INDEX IF EXISTS public.crm_orderitem_ingredient_id_2185a1eb;
DROP INDEX IF EXISTS public.crm_orderitem_dish_id_e3114b2a;
DROP INDEX IF EXISTS public.crm_orderitem_custom_tech_card_id_5e4ea50e;
DROP INDEX IF EXISTS public.crm_order_order_number_16e6bd13_like;
DROP INDEX IF EXISTS public.crm_order_manager_id_039a402f;
DROP INDEX IF EXISTS public.crm_order_client_id_8ed70023;
DROP INDEX IF EXISTS public.crm_interaction_manager_id_24afb2b9;
DROP INDEX IF EXISTS public.crm_interaction_client_id_e63a8170;
DROP INDEX IF EXISTS public.crm_ingredientreservation_order_id_17138f75;
DROP INDEX IF EXISTS public.crm_ingredientreservation_ingredient_id_a8564254;
DROP INDEX IF EXISTS public.crm_ingredient_name_cd2f75d5_like;
DROP INDEX IF EXISTS public.crm_equipmentreservation_order_id_e9f68c20;
DROP INDEX IF EXISTS public.crm_equipmentreservation_equipment_id_01460725;
DROP INDEX IF EXISTS public.crm_dishequipmentrequirement_equipment_id_c03741cd;
DROP INDEX IF EXISTS public.crm_dishequipmentrequirement_dish_id_d09c1cdf;
DROP INDEX IF EXISTS public.crm_dish_created_by_id_1ec5aa20;
DROP INDEX IF EXISTS public.crm_delivery_route_id_7a215b73;
DROP INDEX IF EXISTS public.crm_delivery_order_id_88ce6731;
DROP INDEX IF EXISTS public.crm_delivery_courier_id_fa676b65;
DROP INDEX IF EXISTS public.crm_courierassignment_route_id_40d05eac;
DROP INDEX IF EXISTS public.crm_courierassignment_courier_id_d66fb584;
DROP INDEX IF EXISTS public.crm_clientstagehistory_stage_id_04e1997a;
DROP INDEX IF EXISTS public.crm_clientstagehistory_client_id_926d0169;
DROP INDEX IF EXISTS public.crm_clientstagehistory_changed_by_id_84f6d086;
DROP INDEX IF EXISTS public.crm_clientcontact_client_id_b44e105e;
DROP INDEX IF EXISTS public.crm_clientallowedtechcard_tech_card_id_4956fc6d;
DROP INDEX IF EXISTS public.crm_clientallowedtechcard_client_id_a202bbc1;
DROP INDEX IF EXISTS public.crm_client_responsible_manager_id_7081e9b4;
DROP INDEX IF EXISTS public.crm_client_current_stage_id_e8a55701;
DROP INDEX IF EXISTS public.crm_auditlog_actor_id_4382924f;
DROP INDEX IF EXISTS public.communications_entitycomment_content_type_id_71d2a881;
DROP INDEX IF EXISTS public.communications_entitycomment_author_id_b58bd8f7;
DROP INDEX IF EXISTS public.communications_directmessage_sender_id_5355d0f2;
DROP INDEX IF EXISTS public.communications_directmessage_recipient_id_267e91bf;
DROP INDEX IF EXISTS public.communicati_sender__0f8c80_idx;
DROP INDEX IF EXISTS public.communicati_recipie_c7ddb4_idx;
DROP INDEX IF EXISTS public.communicati_content_67dfbc_idx;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.admin_panel_backup_created_by_id_f9e87668;
ALTER TABLE IF EXISTS ONLY public.reports_report DROP CONSTRAINT IF EXISTS reports_report_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_userrole DROP CONSTRAINT IF EXISTS crm_userrole_user_id_role_id_fa7b18da_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_userrole DROP CONSTRAINT IF EXISTS crm_userrole_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_user DROP CONSTRAINT IF EXISTS crm_user_username_key;
ALTER TABLE IF EXISTS ONLY public.crm_user_user_permissions DROP CONSTRAINT IF EXISTS crm_user_user_permissions_user_id_permission_id_72b1e4e1_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_user_user_permissions DROP CONSTRAINT IF EXISTS crm_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_user DROP CONSTRAINT IF EXISTS crm_user_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_user_groups DROP CONSTRAINT IF EXISTS crm_user_groups_user_id_group_id_56d4cc88_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_user_groups DROP CONSTRAINT IF EXISTS crm_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_user DROP CONSTRAINT IF EXISTS crm_user_email_key;
ALTER TABLE IF EXISTS ONLY public.crm_techcardvariant DROP CONSTRAINT IF EXISTS crm_techcardvariant_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_techcardcomponent DROP CONSTRAINT IF EXISTS crm_techcardcomponent_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_techcard DROP CONSTRAINT IF EXISTS crm_techcard_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_techcard DROP CONSTRAINT IF EXISTS crm_techcard_dish_id_version_label_b05cfe34_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_routestop DROP CONSTRAINT IF EXISTS crm_routestop_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_route DROP CONSTRAINT IF EXISTS crm_route_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_role DROP CONSTRAINT IF EXISTS crm_role_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_role DROP CONSTRAINT IF EXISTS crm_role_name_key;
ALTER TABLE IF EXISTS ONLY public.crm_productionreservation DROP CONSTRAINT IF EXISTS crm_productionreservation_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_pickingsession DROP CONSTRAINT IF EXISTS crm_pickingsession_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_pickingsession DROP CONSTRAINT IF EXISTS crm_pickingsession_order_id_key;
ALTER TABLE IF EXISTS ONLY public.crm_orderitem DROP CONSTRAINT IF EXISTS crm_orderitem_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_order DROP CONSTRAINT IF EXISTS crm_order_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_order DROP CONSTRAINT IF EXISTS crm_order_order_number_key;
ALTER TABLE IF EXISTS ONLY public.crm_logisticianprofile DROP CONSTRAINT IF EXISTS crm_logisticianprofile_user_id_key;
ALTER TABLE IF EXISTS ONLY public.crm_logisticianprofile DROP CONSTRAINT IF EXISTS crm_logisticianprofile_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_interaction DROP CONSTRAINT IF EXISTS crm_interaction_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientstock DROP CONSTRAINT IF EXISTS crm_ingredientstock_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientstock DROP CONSTRAINT IF EXISTS crm_ingredientstock_ingredient_id_key;
ALTER TABLE IF EXISTS ONLY public.crm_ingredientreservation DROP CONSTRAINT IF EXISTS crm_ingredientreservation_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_ingredient DROP CONSTRAINT IF EXISTS crm_ingredient_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_ingredient DROP CONSTRAINT IF EXISTS crm_ingredient_name_key;
ALTER TABLE IF EXISTS ONLY public.crm_equipmentreservation DROP CONSTRAINT IF EXISTS crm_equipmentreservation_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_equipment DROP CONSTRAINT IF EXISTS crm_equipment_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_dishequipmentrequirement DROP CONSTRAINT IF EXISTS crm_dishequipmentrequirement_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_dishequipmentrequirement DROP CONSTRAINT IF EXISTS crm_dishequipmentrequirement_dish_id_equipment_id_03d5c14f_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_dish DROP CONSTRAINT IF EXISTS crm_dish_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_delivery DROP CONSTRAINT IF EXISTS crm_delivery_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_courierassignment DROP CONSTRAINT IF EXISTS crm_courierassignment_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_courierassignment DROP CONSTRAINT IF EXISTS crm_courierassignment_courier_id_route_id_4ca14639_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_courier DROP CONSTRAINT IF EXISTS crm_courier_user_id_key;
ALTER TABLE IF EXISTS ONLY public.crm_courier DROP CONSTRAINT IF EXISTS crm_courier_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_cooperationstage DROP CONSTRAINT IF EXISTS crm_cooperationstage_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_clientstagehistory DROP CONSTRAINT IF EXISTS crm_clientstagehistory_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_clientcontact DROP CONSTRAINT IF EXISTS crm_clientcontact_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_clientallowedtechcard DROP CONSTRAINT IF EXISTS crm_clientallowedtechcard_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_clientallowedtechcard DROP CONSTRAINT IF EXISTS crm_clientallowedtechcard_client_id_tech_card_id_f1bfd130_uniq;
ALTER TABLE IF EXISTS ONLY public.crm_client DROP CONSTRAINT IF EXISTS crm_client_pkey;
ALTER TABLE IF EXISTS ONLY public.crm_auditlog DROP CONSTRAINT IF EXISTS crm_auditlog_pkey;
ALTER TABLE IF EXISTS ONLY public.communications_entitycomment DROP CONSTRAINT IF EXISTS communications_entitycomment_pkey;
ALTER TABLE IF EXISTS ONLY public.communications_directmessage DROP CONSTRAINT IF EXISTS communications_directmessage_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.admin_panel_backupschedule DROP CONSTRAINT IF EXISTS admin_panel_backupschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.admin_panel_backup DROP CONSTRAINT IF EXISTS admin_panel_backup_pkey;
DROP TABLE IF EXISTS public.reports_report;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.crm_userrole;
DROP TABLE IF EXISTS public.crm_user_user_permissions;
DROP TABLE IF EXISTS public.crm_user_groups;
DROP TABLE IF EXISTS public.crm_user;
DROP TABLE IF EXISTS public.crm_techcardvariant;
DROP TABLE IF EXISTS public.crm_techcardcomponent;
DROP TABLE IF EXISTS public.crm_techcard;
DROP TABLE IF EXISTS public.crm_routestop;
DROP TABLE IF EXISTS public.crm_route;
DROP TABLE IF EXISTS public.crm_role;
DROP TABLE IF EXISTS public.crm_productionreservation;
DROP TABLE IF EXISTS public.crm_pickingsession;
DROP TABLE IF EXISTS public.crm_orderitem;
DROP TABLE IF EXISTS public.crm_order;
DROP TABLE IF EXISTS public.crm_logisticianprofile;
DROP TABLE IF EXISTS public.crm_interaction;
DROP TABLE IF EXISTS public.crm_ingredientstock;
DROP TABLE IF EXISTS public.crm_ingredientreservation;
DROP TABLE IF EXISTS public.crm_ingredient;
DROP TABLE IF EXISTS public.crm_equipmentreservation;
DROP TABLE IF EXISTS public.crm_equipment;
DROP TABLE IF EXISTS public.crm_dishequipmentrequirement;
DROP TABLE IF EXISTS public.crm_dish;
DROP TABLE IF EXISTS public.crm_delivery;
DROP TABLE IF EXISTS public.crm_courierassignment;
DROP TABLE IF EXISTS public.crm_courier;
DROP TABLE IF EXISTS public.crm_cooperationstage;
DROP TABLE IF EXISTS public.crm_clientstagehistory;
DROP TABLE IF EXISTS public.crm_clientcontact;
DROP TABLE IF EXISTS public.crm_clientallowedtechcard;
DROP TABLE IF EXISTS public.crm_client;
DROP TABLE IF EXISTS public.crm_auditlog;
DROP TABLE IF EXISTS public.communications_entitycomment;
DROP TABLE IF EXISTS public.communications_directmessage;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.admin_panel_backupschedule;
DROP TABLE IF EXISTS public.admin_panel_backup;
DROP FUNCTION IF EXISTS public.crm_tg_validate_delivery_date();
DROP FUNCTION IF EXISTS public.crm_tg_prepare_orderitem();
DROP FUNCTION IF EXISTS public.crm_tg_orderitem_total_recalc();
DROP FUNCTION IF EXISTS public.crm_tg_check_ingredient_reservation();
DROP PROCEDURE IF EXISTS public.crm_set_order_status(IN p_order_id bigint, IN p_status character varying);
DROP FUNCTION IF EXISTS public.crm_recalculate_order_total(p_order_id bigint);
-- *not* dropping schema, since initdb creates it
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: crm_recalculate_order_total(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crm_recalculate_order_total(p_order_id bigint) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    SELECT COALESCE(SUM(line_total), 0)
      INTO v_total
      FROM crm_orderitem
     WHERE order_id = p_order_id;

    UPDATE crm_order
       SET total_amount = v_total
     WHERE id = p_order_id;

    RETURN v_total;
END;
$$;


--
-- Name: crm_set_order_status(bigint, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.crm_set_order_status(IN p_order_id bigint, IN p_status character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE crm_order
       SET status = p_status,
           updated_at = NOW()
     WHERE id = p_order_id;
END;
$$;


--
-- Name: crm_tg_check_ingredient_reservation(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crm_tg_check_ingredient_reservation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_reserved NUMERIC;
    v_stock NUMERIC;
BEGIN
    SELECT COALESCE(SUM(quantity), 0)
      INTO v_reserved
      FROM crm_ingredientreservation
     WHERE ingredient_id = NEW.ingredient_id
       AND production_date = NEW.production_date
       AND id <> COALESCE(NEW.id, -1);

    SELECT COALESCE(quantity, 0)
      INTO v_stock
      FROM crm_ingredientstock
     WHERE ingredient_id = NEW.ingredient_id;

    IF (v_reserved + NEW.quantity) > v_stock THEN
        RAISE EXCEPTION 'insufficient ingredient stock for ingredient_id=% and production_date=%',
            NEW.ingredient_id, NEW.production_date
            USING ERRCODE = '22000';
    END IF;

    RETURN NEW;
END;
$$;


--
-- Name: crm_tg_orderitem_total_recalc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crm_tg_orderitem_total_recalc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        PERFORM crm_recalculate_order_total(OLD.order_id);
    ELSE
        PERFORM crm_recalculate_order_total(NEW.order_id);
    END IF;
    RETURN NULL;
END;
$$;


--
-- Name: crm_tg_prepare_orderitem(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crm_tg_prepare_orderitem() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.quantity <= 0 THEN
        RAISE EXCEPTION 'quantity must be greater than 0'
            USING ERRCODE = '22023';
    END IF;

    IF NEW.unit_price < 0 THEN
        RAISE EXCEPTION 'unit_price cannot be negative'
            USING ERRCODE = '22023';
    END IF;

    NEW.line_total := ROUND(NEW.quantity * NEW.unit_price, 2);
    RETURN NEW;
END;
$$;


--
-- Name: crm_tg_validate_delivery_date(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crm_tg_validate_delivery_date() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.delivery_date IS NOT NULL AND NEW.delivery_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'delivery_date (%) cannot be in the past', NEW.delivery_date
            USING ERRCODE = '22007';
    END IF;
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_panel_backup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_panel_backup (
    id bigint NOT NULL,
    file_path character varying(500) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by_id bigint
);


--
-- Name: admin_panel_backup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.admin_panel_backup ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_panel_backup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: admin_panel_backupschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_panel_backupschedule (
    id bigint NOT NULL,
    frequency character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: admin_panel_backupschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.admin_panel_backupschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.admin_panel_backupschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: communications_directmessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communications_directmessage (
    id bigint NOT NULL,
    body text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    read_at timestamp with time zone,
    recipient_id bigint NOT NULL,
    sender_id bigint NOT NULL
);


--
-- Name: communications_directmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.communications_directmessage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.communications_directmessage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: communications_entitycomment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communications_entitycomment (
    id bigint NOT NULL,
    object_id integer NOT NULL,
    body text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    author_id bigint NOT NULL,
    content_type_id integer NOT NULL,
    CONSTRAINT communications_entitycomment_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: communications_entitycomment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.communications_entitycomment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.communications_entitycomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_auditlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_auditlog (
    id bigint NOT NULL,
    actor_role character varying(64) NOT NULL,
    object_type character varying(64) NOT NULL,
    object_id integer NOT NULL,
    field_name character varying(64) NOT NULL,
    old_value text NOT NULL,
    new_value text NOT NULL,
    reason text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    actor_id bigint,
    CONSTRAINT crm_auditlog_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: crm_auditlog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_auditlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_auditlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_client; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_client (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    client_type character varying(32) NOT NULL,
    inn character varying(20) NOT NULL,
    kpp character varying(20) NOT NULL,
    default_delivery_address character varying(255) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(32) NOT NULL,
    status character varying(20) NOT NULL,
    responsible_manager_id bigint,
    current_stage_id bigint,
    created_at timestamp with time zone,
    daily_max_weight_kg numeric(10,2),
    daily_min_qty numeric(10,2),
    guaranteed_volume_kg numeric(10,2)
);


--
-- Name: crm_client_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_client ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_clientallowedtechcard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_clientallowedtechcard (
    id bigint NOT NULL,
    client_id bigint NOT NULL,
    tech_card_id bigint NOT NULL
);


--
-- Name: crm_clientallowedtechcard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_clientallowedtechcard ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_clientallowedtechcard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_clientcontact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_clientcontact (
    id bigint NOT NULL,
    full_name character varying(255) NOT NULL,
    "position" character varying(128) NOT NULL,
    phone character varying(32) NOT NULL,
    email character varying(254) NOT NULL,
    is_primary boolean NOT NULL,
    client_id bigint NOT NULL
);


--
-- Name: crm_clientcontact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_clientcontact ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_clientcontact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_clientstagehistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_clientstagehistory (
    id bigint NOT NULL,
    changed_at timestamp with time zone NOT NULL,
    comment text NOT NULL,
    changed_by_id bigint,
    client_id bigint NOT NULL,
    stage_id bigint
);


--
-- Name: crm_clientstagehistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_clientstagehistory ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_clientstagehistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_cooperationstage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_cooperationstage (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    "order" smallint NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT crm_cooperationstage_order_check CHECK (("order" >= 0))
);


--
-- Name: crm_cooperationstage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_cooperationstage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_cooperationstage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_courier; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_courier (
    id bigint NOT NULL,
    transport_type character varying(64) NOT NULL,
    experience_years smallint NOT NULL,
    status character varying(20) NOT NULL,
    user_id bigint NOT NULL,
    zone character varying(128) NOT NULL,
    payload_capacity_kg numeric(10,2),
    cargo_volume_m3 numeric(10,2),
    cargo_length_cm numeric(10,2),
    cargo_width_cm numeric(10,2),
    cargo_height_cm numeric(10,2),
    current_lat numeric(9,6),
    current_lng numeric(9,6),
    location_updated_at timestamp with time zone,
    current_latitude numeric(9,6),
    current_longitude numeric(9,6),
    max_volume numeric(10,2),
    max_weight numeric(10,2),
    CONSTRAINT crm_courier_experience_years_check CHECK ((experience_years >= 0))
);


--
-- Name: crm_courier_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_courier ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_courier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_courierassignment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_courierassignment (
    id bigint NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    courier_id bigint NOT NULL,
    route_id bigint NOT NULL
);


--
-- Name: crm_courierassignment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_courierassignment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_courierassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_delivery; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_delivery (
    id bigint NOT NULL,
    departure_time timestamp with time zone,
    delivered_at timestamp with time zone,
    address character varying(255) NOT NULL,
    note text NOT NULL,
    is_sent boolean NOT NULL,
    courier_id bigint,
    order_id bigint NOT NULL,
    planned_at timestamp with time zone,
    route_id bigint,
    status character varying(20) NOT NULL,
    cargo_weight_kg numeric(10,2),
    cargo_volume_m3 numeric(10,2),
    cargo_length_cm numeric(10,2),
    cargo_width_cm numeric(10,2),
    cargo_height_cm numeric(10,2),
    delivery_date date
);


--
-- Name: crm_delivery_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_delivery ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_delivery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_dish; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_dish (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    unit character varying(32) NOT NULL,
    is_active boolean NOT NULL,
    created_by_id bigint,
    batch_multiple_qty numeric(10,3),
    min_batch_qty numeric(10,3),
    unit_weight_kg numeric(10,3),
    default_price numeric(12,2),
    base_uom character varying(8) NOT NULL,
    quantity_scale smallint NOT NULL,
    daily_capacity numeric(12,3),
    CONSTRAINT crm_dish_quantity_scale_check CHECK ((quantity_scale >= 0))
);


--
-- Name: crm_dish_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_dish ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_dish_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_dishequipmentrequirement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_dishequipmentrequirement (
    id bigint NOT NULL,
    minutes_per_unit numeric(10,2) NOT NULL,
    dish_id bigint NOT NULL,
    equipment_id bigint NOT NULL
);


--
-- Name: crm_dishequipmentrequirement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_dishequipmentrequirement ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_dishequipmentrequirement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_equipment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_equipment (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    capacity_per_hour numeric(10,2),
    available_hours numeric(10,2)
);


--
-- Name: crm_equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_equipment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_equipment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_equipmentreservation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_equipmentreservation (
    id bigint NOT NULL,
    production_date date NOT NULL,
    hours numeric(10,2) NOT NULL,
    equipment_id bigint NOT NULL,
    order_id bigint NOT NULL
);


--
-- Name: crm_equipmentreservation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_equipmentreservation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_equipmentreservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_ingredient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_ingredient (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: crm_ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_ingredient ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_ingredient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_ingredientreservation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_ingredientreservation (
    id bigint NOT NULL,
    production_date date NOT NULL,
    quantity numeric(12,3) NOT NULL,
    ingredient_id bigint NOT NULL,
    order_id bigint NOT NULL
);


--
-- Name: crm_ingredientreservation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_ingredientreservation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_ingredientreservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_ingredientstock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_ingredientstock (
    id bigint NOT NULL,
    quantity numeric(12,3) NOT NULL,
    ingredient_id bigint NOT NULL
);


--
-- Name: crm_ingredientstock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_ingredientstock ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_ingredientstock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_interaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_interaction (
    id bigint NOT NULL,
    interaction_type character varying(20) NOT NULL,
    note text NOT NULL,
    happened_at timestamp with time zone NOT NULL,
    client_id bigint NOT NULL,
    manager_id bigint
);


--
-- Name: crm_interaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_interaction ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_interaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_logisticianprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_logisticianprofile (
    id bigint NOT NULL,
    region character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    transport_types jsonb NOT NULL,
    timezone character varying(64) NOT NULL,
    map_show_traffic boolean NOT NULL,
    preferred_route_type character varying(16) NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: crm_logisticianprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_logisticianprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_logisticianprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_order (
    id bigint NOT NULL,
    order_number character varying(50) NOT NULL,
    address character varying(255) NOT NULL,
    status character varying(64) NOT NULL,
    comments text NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    client_id bigint NOT NULL,
    manager_id bigint,
    is_archived boolean NOT NULL,
    delivery_date date,
    delivery_time time without time zone,
    delivery_type character varying(32) NOT NULL,
    production_date date,
    production_shift character varying(32) NOT NULL,
    production_window_end time without time zone,
    production_window_start time without time zone
);


--
-- Name: crm_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_order ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_orderitem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_orderitem (
    id bigint NOT NULL,
    quantity numeric(10,3) NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    line_total numeric(12,2) NOT NULL,
    supply_type character varying(64) NOT NULL,
    dish_id bigint,
    ingredient_id bigint,
    order_id bigint NOT NULL,
    custom_tech_card_id bigint,
    picked_quantity numeric(10,3) NOT NULL,
    item_status character varying(20) NOT NULL,
    item_comment character varying(255) NOT NULL,
    replacement_text character varying(255) NOT NULL
);


--
-- Name: crm_orderitem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_orderitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_orderitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_pickingsession; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_pickingsession (
    id bigint NOT NULL,
    note text NOT NULL,
    started_at timestamp with time zone,
    finished_at timestamp with time zone,
    updated_at timestamp with time zone NOT NULL,
    order_id bigint NOT NULL,
    picker_id bigint
);


--
-- Name: crm_pickingsession_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_pickingsession ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_pickingsession_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_productionreservation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_productionreservation (
    id bigint NOT NULL,
    production_date date NOT NULL,
    weight_kg numeric(12,3) NOT NULL,
    order_id bigint NOT NULL
);


--
-- Name: crm_productionreservation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_productionreservation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_productionreservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_role (
    id bigint NOT NULL,
    name character varying(64) NOT NULL
);


--
-- Name: crm_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_role ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_route; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_route (
    id bigint NOT NULL,
    planned_date date NOT NULL,
    status character varying(20) NOT NULL,
    notes text NOT NULL,
    logistician_id bigint,
    max_duration_minutes smallint NOT NULL,
    soft_limit_stops smallint NOT NULL,
    strict_mode boolean NOT NULL,
    CONSTRAINT crm_route_max_duration_minutes_check CHECK ((max_duration_minutes >= 0)),
    CONSTRAINT crm_route_soft_limit_stops_check CHECK ((soft_limit_stops >= 0))
);


--
-- Name: crm_route_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_route ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_route_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_routestop; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_routestop (
    id bigint NOT NULL,
    sequence_index smallint NOT NULL,
    planned_time timestamp with time zone,
    actual_time timestamp with time zone,
    note character varying(255) NOT NULL,
    delivery_id bigint NOT NULL,
    route_id bigint NOT NULL,
    latitude numeric(9,6),
    longitude numeric(9,6),
    status character varying(20) NOT NULL,
    delivery_date date,
    failure_reason text NOT NULL,
    proof_of_delivery character varying(100),
    proof_uploaded_at timestamp with time zone,
    proof_uploaded_by_id bigint,
    service_time_minutes smallint NOT NULL,
    proof_review_comment text NOT NULL,
    proof_review_status character varying(32) NOT NULL,
    proof_reviewed_at timestamp with time zone,
    proof_reviewed_by_id bigint,
    CONSTRAINT crm_routestop_sequence_index_check CHECK ((sequence_index >= 0)),
    CONSTRAINT crm_routestop_service_time_minutes_check CHECK ((service_time_minutes >= 0))
);


--
-- Name: crm_routestop_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_routestop ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_routestop_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_techcard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_techcard (
    id bigint NOT NULL,
    version_label character varying(32) NOT NULL,
    description text NOT NULL,
    photo_url character varying(200) NOT NULL,
    is_active boolean NOT NULL,
    approved_by_id bigint,
    dish_id bigint NOT NULL
);


--
-- Name: crm_techcard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_techcard ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_techcard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_techcardcomponent; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_techcardcomponent (
    id bigint NOT NULL,
    quantity numeric(10,3) NOT NULL,
    note character varying(255) NOT NULL,
    ingredient_id bigint NOT NULL,
    tech_card_id bigint NOT NULL
);


--
-- Name: crm_techcardcomponent_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_techcardcomponent ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_techcardcomponent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_techcardvariant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_techcardvariant (
    id bigint NOT NULL,
    quantity numeric(10,3) NOT NULL,
    note character varying(255) NOT NULL,
    tech_card_id bigint NOT NULL
);


--
-- Name: crm_techcardvariant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_techcardvariant ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_techcardvariant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    full_name character varying(255) NOT NULL,
    phone character varying(32) NOT NULL
);


--
-- Name: crm_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: crm_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: crm_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: crm_userrole; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crm_userrole (
    id bigint NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    role_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: crm_userrole_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.crm_userrole ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.crm_userrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: reports_report; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reports_report (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    period_from date NOT NULL,
    period_to date NOT NULL,
    status character varying(20) NOT NULL,
    file character varying(100),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id bigint,
    validation_status character varying(20) NOT NULL,
    validation_message text NOT NULL
);


--
-- Name: reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.reports_report ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reports_report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: admin_panel_backupschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin_panel_backupschedule (id, frequency, is_active, updated_at) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	2	add_permission
2	Can change permission	2	change_permission
3	Can delete permission	2	delete_permission
4	Can view permission	2	view_permission
5	Can add group	1	add_group
6	Can change group	1	change_group
7	Can delete group	1	delete_group
8	Can view group	1	view_group
9	Can add content type	3	add_contenttype
10	Can change content type	3	change_contenttype
11	Can delete content type	3	delete_contenttype
12	Can view content type	3	view_contenttype
13	Can add session	4	add_session
14	Can change session	4	change_session
15	Can delete session	4	delete_session
16	Can view session	4	view_session
17	Can add Этап сотрудничества	10	add_cooperationstage
18	Can change Этап сотрудничества	10	change_cooperationstage
19	Can delete Этап сотрудничества	10	delete_cooperationstage
20	Can view Этап сотрудничества	10	view_cooperationstage
21	Can add Ингредиент	18	add_ingredient
22	Can change Ингредиент	18	change_ingredient
23	Can delete Ингредиент	18	delete_ingredient
24	Can view Ингредиент	18	view_ingredient
25	Can add Роль	27	add_role
26	Can change Роль	27	change_role
27	Can delete Роль	27	delete_role
28	Can view Роль	27	view_role
29	Can add Пользователь	33	add_user
30	Can change Пользователь	33	change_user
31	Can delete Пользователь	33	delete_user
32	Can view Пользователь	33	view_user
33	Can add Клиент	6	add_client
34	Can change Клиент	6	change_client
35	Can delete Клиент	6	delete_client
36	Can view Клиент	6	view_client
37	Can add Контакт клиента	8	add_clientcontact
38	Can change Контакт клиента	8	change_clientcontact
39	Can delete Контакт клиента	8	delete_clientcontact
40	Can view Контакт клиента	8	view_clientcontact
41	Can add История этапов клиента	9	add_clientstagehistory
42	Can change История этапов клиента	9	change_clientstagehistory
43	Can delete История этапов клиента	9	delete_clientstagehistory
44	Can view История этапов клиента	9	view_clientstagehistory
45	Can add Курьер	11	add_courier
46	Can change Курьер	11	change_courier
47	Can delete Курьер	11	delete_courier
48	Can view Курьер	11	view_courier
49	Can add Блюдо каталога	14	add_dish
50	Can change Блюдо каталога	14	change_dish
51	Can delete Блюдо каталога	14	delete_dish
52	Can view Блюдо каталога	14	view_dish
53	Can add Взаимодействие	21	add_interaction
54	Can change Взаимодействие	21	change_interaction
55	Can delete Взаимодействие	21	delete_interaction
56	Can view Взаимодействие	21	view_interaction
57	Can add Заказ	23	add_order
58	Can change Заказ	23	change_order
59	Can delete Заказ	23	delete_order
60	Can view Заказ	23	view_order
61	Can add Доставка	13	add_delivery
62	Can change Доставка	13	change_delivery
63	Can delete Доставка	13	delete_delivery
64	Can view Доставка	13	view_delivery
65	Can add Маршрут	28	add_route
66	Can change Маршрут	28	change_route
67	Can delete Маршрут	28	delete_route
68	Can view Маршрут	28	view_route
69	Can add Остановка маршрута	29	add_routestop
70	Can change Остановка маршрута	29	change_routestop
71	Can delete Остановка маршрута	29	delete_routestop
72	Can view Остановка маршрута	29	view_routestop
73	Can add Техкарта блюда	30	add_techcard
74	Can change Техкарта блюда	30	change_techcard
75	Can delete Техкарта блюда	30	delete_techcard
76	Can view Техкарта блюда	30	view_techcard
77	Can add Позиция заказа	24	add_orderitem
78	Can change Позиция заказа	24	change_orderitem
79	Can delete Позиция заказа	24	delete_orderitem
80	Can view Позиция заказа	24	view_orderitem
81	Can add Состав техкарты	31	add_techcardcomponent
82	Can change Состав техкарты	31	change_techcardcomponent
83	Can delete Состав техкарты	31	delete_techcardcomponent
84	Can view Состав техкарты	31	view_techcardcomponent
85	Can add Сорт/вариант техкарты	32	add_techcardvariant
86	Can change Сорт/вариант техкарты	32	change_techcardvariant
87	Can delete Сорт/вариант техкарты	32	delete_techcardvariant
88	Can view Сорт/вариант техкарты	32	view_techcardvariant
89	Can add Роль пользователя	34	add_userrole
90	Can change Роль пользователя	34	change_userrole
91	Can delete Роль пользователя	34	delete_userrole
92	Can view Роль пользователя	34	view_userrole
93	Can add Назначение курьера	12	add_courierassignment
94	Can change Назначение курьера	12	change_courierassignment
95	Can delete Назначение курьера	12	delete_courierassignment
96	Can view Назначение курьера	12	view_courierassignment
97	Can add Сборка заказа	25	add_pickingsession
98	Can change Сборка заказа	25	change_pickingsession
99	Can delete Сборка заказа	25	delete_pickingsession
100	Can view Сборка заказа	25	view_pickingsession
101	Can add Профиль логиста	22	add_logisticianprofile
102	Can change Профиль логиста	22	change_logisticianprofile
103	Can delete Профиль логиста	22	delete_logisticianprofile
104	Can view Профиль логиста	22	view_logisticianprofile
105	Can add Аудит	5	add_auditlog
106	Can change Аудит	5	change_auditlog
107	Can delete Аудит	5	delete_auditlog
108	Can view Аудит	5	view_auditlog
109	Can add Оборудование	16	add_equipment
110	Can change Оборудование	16	change_equipment
111	Can delete Оборудование	16	delete_equipment
112	Can view Оборудование	16	view_equipment
113	Can add Резерв оборудования	17	add_equipmentreservation
114	Can change Резерв оборудования	17	change_equipmentreservation
115	Can delete Резерв оборудования	17	delete_equipmentreservation
116	Can view Резерв оборудования	17	view_equipmentreservation
117	Can add Резерв ингредиента	19	add_ingredientreservation
118	Can change Резерв ингредиента	19	change_ingredientreservation
119	Can delete Резерв ингредиента	19	delete_ingredientreservation
120	Can view Резерв ингредиента	19	view_ingredientreservation
121	Can add Остаток ингредиента	20	add_ingredientstock
122	Can change Остаток ингредиента	20	change_ingredientstock
123	Can delete Остаток ингредиента	20	delete_ingredientstock
124	Can view Остаток ингредиента	20	view_ingredientstock
125	Can add Резерв мощности производства	26	add_productionreservation
126	Can change Резерв мощности производства	26	change_productionreservation
127	Can delete Резерв мощности производства	26	delete_productionreservation
128	Can view Резерв мощности производства	26	view_productionreservation
129	Can add Разрешённая техкарта клиента	7	add_clientallowedtechcard
130	Can change Разрешённая техкарта клиента	7	change_clientallowedtechcard
131	Can delete Разрешённая техкарта клиента	7	delete_clientallowedtechcard
132	Can view Разрешённая техкарта клиента	7	view_clientallowedtechcard
133	Can add Требование оборудования	15	add_dishequipmentrequirement
134	Can change Требование оборудования	15	change_dishequipmentrequirement
135	Can delete Требование оборудования	15	delete_dishequipmentrequirement
136	Can view Требование оборудования	15	view_dishequipmentrequirement
137	Can add report	35	add_report
138	Can change report	35	change_report
139	Can delete report	35	delete_report
140	Can view report	35	view_report
141	Can add backup	36	add_backup
142	Can change backup	36	change_backup
143	Can delete backup	36	delete_backup
144	Can view backup	36	view_backup
145	Can add backup schedule	37	add_backupschedule
146	Can change backup schedule	37	change_backupschedule
147	Can delete backup schedule	37	delete_backupschedule
148	Can view backup schedule	37	view_backupschedule
149	Can add Личное сообщение	38	add_directmessage
150	Can change Личное сообщение	38	change_directmessage
151	Can delete Личное сообщение	38	delete_directmessage
152	Can view Личное сообщение	38	view_directmessage
153	Can add Комментарий к сущности	39	add_entitycomment
154	Can change Комментарий к сущности	39	change_entitycomment
155	Can delete Комментарий к сущности	39	delete_entitycomment
156	Can view Комментарий к сущности	39	view_entitycomment
\.


--
-- Data for Name: communications_directmessage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.communications_directmessage (id, body, created_at, read_at, recipient_id, sender_id) FROM stdin;
\.


--
-- Data for Name: communications_entitycomment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.communications_entitycomment (id, object_id, body, created_at, updated_at, author_id, content_type_id) FROM stdin;
\.


--
-- Data for Name: crm_auditlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_auditlog (id, actor_role, object_type, object_id, field_name, old_value, new_value, reason, created_at, actor_id) FROM stdin;
\.


--
-- Data for Name: crm_client; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_client (id, name, client_type, inn, kpp, default_delivery_address, email, phone, status, responsible_manager_id, current_stage_id, created_at, daily_max_weight_kg, daily_min_qty, guaranteed_volume_kg) FROM stdin;
1	Ресторан «Красная Площадь»	restaurant	7701000001	770100001	Москва, Красная площадь, 1	demo-client-1@artculinary.local	+79990001001	active	1	1	2026-05-14 11:38:37.134078+03	\N	\N	\N
2	Кафе «Тверская 7»	cafe	7701000002	770100002	Москва, Тверская улица, 7	demo-client-2@artculinary.local	+79990001002	active	1	2	2026-05-14 11:38:37.139926+03	\N	\N	\N
3	Гастробар «Новый Арбат»	restaurant	7701000003	770100003	Москва, Новый Арбат, 15	demo-client-3@artculinary.local	+79990001003	prospect	1	3	2026-05-14 11:38:37.142488+03	\N	\N	\N
4	Бистро «Кутузовский»	cafe	7701000004	770100004	Москва, Кутузовский проспект, 2/1	demo-client-4@artculinary.local	+79990001004	active	1	4	2026-05-14 11:38:37.144818+03	\N	\N	\N
5	Маркет «Ленинградский»	store	7701000005	770100005	Москва, Ленинградский проспект, 36	demo-client-5@artculinary.local	+79990001005	active	1	4	2026-05-14 11:38:37.147531+03	\N	\N	\N
6	Кулинария «Большая Дмитровка»	store	7701000006	770100006	Москва, Большая Дмитровка, 11	demo-client-6@artculinary.local	+79990001006	prospect	1	4	2026-05-14 11:38:37.150621+03	\N	\N	\N
7	Кафе «Мясницкая 24»	cafe	7701000007	770100007	Москва, Мясницкая улица, 24	demo-client-7@artculinary.local	+79990001007	active	1	4	2026-05-14 11:38:37.15399+03	\N	\N	\N
8	Ресторан «Пятницкая»	restaurant	7701000008	770100008	Москва, Пятницкая улица, 25	demo-client-8@artculinary.local	+79990001008	active	1	4	2026-05-14 11:38:37.156404+03	\N	\N	\N
9	Магазин «Земляной Вал»	store	7701000009	770100009	Москва, Земляной Вал, 33	demo-client-9@artculinary.local	+79990001009	prospect	1	4	2026-05-14 11:38:37.158805+03	\N	\N	\N
10	Офисный центр «Пресня»	other	7701000010	770100010	Москва, Пресненская набережная, 12	demo-client-10@artculinary.local	+79990001010	active	1	4	2026-05-14 11:38:37.1623+03	\N	\N	\N
\.


--
-- Data for Name: crm_clientallowedtechcard; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_clientallowedtechcard (id, client_id, tech_card_id) FROM stdin;
\.


--
-- Data for Name: crm_clientcontact; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_clientcontact (id, full_name, "position", phone, email, is_primary, client_id) FROM stdin;
\.


--
-- Data for Name: crm_clientstagehistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_clientstagehistory (id, changed_at, comment, changed_by_id, client_id, stage_id) FROM stdin;
1	2026-05-14 11:38:37.137649+03	Демо-клиент: московская точка доставки	1	1	1
2	2026-05-14 11:38:37.141201+03	Демо-клиент: московская точка доставки	1	2	2
3	2026-05-14 11:38:37.143607+03	Демо-клиент: московская точка доставки	1	3	3
4	2026-05-14 11:38:37.146063+03	Демо-клиент: московская точка доставки	1	4	4
5	2026-05-14 11:38:37.148902+03	Демо-клиент: московская точка доставки	1	5	4
6	2026-05-14 11:38:37.15249+03	Демо-клиент: московская точка доставки	1	6	4
7	2026-05-14 11:38:37.155111+03	Демо-клиент: московская точка доставки	1	7	4
8	2026-05-14 11:38:37.157631+03	Демо-клиент: московская точка доставки	1	8	4
9	2026-05-14 11:38:37.160259+03	Демо-клиент: московская точка доставки	1	9	4
10	2026-05-14 11:38:37.163612+03	Демо-клиент: московская точка доставки	1	10	4
\.


--
-- Data for Name: crm_cooperationstage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_cooperationstage (id, name, "order", is_active) FROM stdin;
1	Лид	1	t
2	Переговоры	2	t
3	Контракт	3	t
4	Сделка	4	t
\.


--
-- Data for Name: crm_courier; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_courier (id, transport_type, experience_years, status, user_id, zone, payload_capacity_kg, cargo_volume_m3, cargo_length_cm, cargo_width_cm, cargo_height_cm, current_lat, current_lng, location_updated_at, current_latitude, current_longitude, max_volume, max_weight) FROM stdin;
1	Авто	3	В рейсе	5	Центр	450.00	4.50	220.00	140.00	140.00	55.755864	37.617698	2026-05-14 11:38:37.403861+03	55.755864	37.617698	4.50	450.00
2	Фургон	3	Свободен	6	Центр-Север	900.00	9.00	220.00	140.00	140.00	55.751244	37.618423	2026-05-14 11:38:37.60302+03	55.751244	37.618423	9.00	900.00
3	Рефрижератор	3	Занят	7	Центр	1200.00	12.00	220.00	140.00	140.00	55.760186	37.609543	2026-05-14 11:38:37.800541+03	55.760186	37.609543	12.00	1200.00
\.


--
-- Data for Name: crm_courierassignment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_courierassignment (id, assigned_at, courier_id, route_id) FROM stdin;
1	2026-05-14 11:38:37.823924+03	1	1
2	2026-05-14 11:38:37.831913+03	2	2
3	2026-05-14 11:38:37.837291+03	3	3
\.


--
-- Data for Name: crm_delivery; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_delivery (id, departure_time, delivered_at, address, note, is_sent, courier_id, order_id, planned_at, route_id, status, cargo_weight_kg, cargo_volume_m3, cargo_length_cm, cargo_width_cm, cargo_height_cm, delivery_date) FROM stdin;
1	\N	\N	Москва, Красная площадь, 1	DEMO_MOSCOW_LOGISTICS	f	1	1	2026-05-14 13:45:00+03	1	Запланировано	21.00	0.50	60.00	40.00	35.00	2026-05-14
2	\N	\N	Москва, Тверская улица, 7	DEMO_MOSCOW_LOGISTICS	f	1	2	2026-05-14 14:10:00+03	1	В пути	24.00	0.60	60.00	40.00	35.00	2026-05-14
6	\N	\N	Москва, Большая Дмитровка, 11	DEMO_MOSCOW_LOGISTICS	f	1	6	2026-05-14 14:35:00+03	1	В пути	36.00	1.00	60.00	40.00	35.00	2026-05-14
5	\N	\N	Москва, Ленинградский проспект, 36	DEMO_MOSCOW_LOGISTICS	f	2	5	2026-05-14 14:00:00+03	2	Запланировано	33.00	0.90	60.00	40.00	35.00	2026-05-14
7	\N	\N	Москва, Мясницкая улица, 24	DEMO_MOSCOW_LOGISTICS	f	2	7	2026-05-14 14:25:00+03	2	Запланировано	39.00	1.10	60.00	40.00	35.00	2026-05-14
9	\N	\N	Москва, Земляной Вал, 33	DEMO_MOSCOW_LOGISTICS	f	2	9	2026-05-14 14:50:00+03	2	Доставлено	45.00	1.30	60.00	40.00	35.00	2026-05-14
3	\N	\N	Москва, Новый Арбат, 15	DEMO_MOSCOW_LOGISTICS	f	3	3	2026-05-14 14:15:00+03	3	Запланировано	27.00	0.70	60.00	40.00	35.00	2026-05-14
4	\N	\N	Москва, Кутузовский проспект, 2/1	DEMO_MOSCOW_LOGISTICS	f	3	4	2026-05-14 14:40:00+03	3	Доставлено	30.00	0.80	60.00	40.00	35.00	2026-05-14
8	\N	\N	Москва, Пятницкая улица, 25	DEMO_MOSCOW_LOGISTICS	f	3	8	2026-05-14 15:05:00+03	3	Запланировано	42.00	1.20	60.00	40.00	35.00	2026-05-14
10	\N	\N	Москва, Пресненская набережная, 12	DEMO_MOSCOW_LOGISTICS	f	3	10	2026-05-14 15:30:00+03	3	Запланировано	48.00	1.40	60.00	40.00	35.00	2026-05-14
\.


--
-- Data for Name: crm_dish; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_dish (id, name, unit, is_active, created_by_id, batch_multiple_qty, min_batch_qty, unit_weight_kg, default_price, base_uom, quantity_scale, daily_capacity) FROM stdin;
\.


--
-- Data for Name: crm_dishequipmentrequirement; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_dishequipmentrequirement (id, minutes_per_unit, dish_id, equipment_id) FROM stdin;
\.


--
-- Data for Name: crm_equipment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_equipment (id, name, capacity_per_hour, available_hours) FROM stdin;
\.


--
-- Data for Name: crm_equipmentreservation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_equipmentreservation (id, production_date, hours, equipment_id, order_id) FROM stdin;
\.


--
-- Data for Name: crm_ingredient; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_ingredient (id, name, is_active) FROM stdin;
\.


--
-- Data for Name: crm_ingredientreservation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_ingredientreservation (id, production_date, quantity, ingredient_id, order_id) FROM stdin;
\.


--
-- Data for Name: crm_ingredientstock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_ingredientstock (id, quantity, ingredient_id) FROM stdin;
\.


--
-- Data for Name: crm_interaction; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_interaction (id, interaction_type, note, happened_at, client_id, manager_id) FROM stdin;
1	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.16421+03	1	1
2	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.167323+03	2	1
3	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.169037+03	3	1
4	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.170382+03	4	1
5	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.171479+03	5	1
6	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.172556+03	6	1
7	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.174123+03	7	1
8	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.17556+03	8	1
9	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.177164+03	9	1
10	call	Демо: согласование регулярных поставок	2026-05-14 11:38:37.178738+03	10	1
\.


--
-- Data for Name: crm_logisticianprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_logisticianprofile (id, region, city, transport_types, timezone, map_show_traffic, preferred_route_type, user_id) FROM stdin;
1	Москва	Москва	["car", "van", "refrigerated"]	Europe/Moscow	t	fastest	2
\.


--
-- Data for Name: crm_order; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_order (id, order_number, address, status, comments, total_amount, created_at, updated_at, client_id, manager_id, is_archived, delivery_date, delivery_time, delivery_type, production_date, production_shift, production_window_end, production_window_start) FROM stdin;
1	ORD-DEMO-MSK-01	Москва, Красная площадь, 1	На проверке	DEMO_MOSCOW_LOGISTICS	19750.00	2026-05-14 11:38:37.18346+03	2026-05-14 11:38:37.183475+03	1	1	f	2026-05-14	10:25:00	Разовая	\N		\N	\N
2	ORD-DEMO-MSK-02	Москва, Тверская улица, 7	Подтвержден производством	DEMO_MOSCOW_LOGISTICS	21500.00	2026-05-14 11:38:37.190469+03	2026-05-14 11:38:37.190474+03	2	1	f	2026-05-14	10:50:00	Регулярная	\N		\N	\N
3	ORD-DEMO-MSK-03	Москва, Новый Арбат, 15	В производстве	DEMO_MOSCOW_LOGISTICS	23250.00	2026-05-14 11:38:37.192418+03	2026-05-14 11:38:37.192423+03	3	1	f	2026-05-14	11:15:00	Разовая	\N		\N	\N
4	ORD-DEMO-MSK-04	Москва, Кутузовский проспект, 2/1	Готов к отгрузке	DEMO_MOSCOW_LOGISTICS	25000.00	2026-05-14 11:38:37.194352+03	2026-05-14 11:38:37.194357+03	4	1	f	2026-05-14	11:40:00	Регулярная	\N		\N	\N
5	ORD-DEMO-MSK-05	Москва, Ленинградский проспект, 36	Отгружен	DEMO_MOSCOW_LOGISTICS	26750.00	2026-05-14 11:38:37.196185+03	2026-05-14 11:38:37.19619+03	5	1	f	2026-05-14	12:05:00	Разовая	\N		\N	\N
6	ORD-DEMO-MSK-06	Москва, Большая Дмитровка, 11	На проверке	DEMO_MOSCOW_LOGISTICS	28500.00	2026-05-14 11:38:37.198121+03	2026-05-14 11:38:37.198126+03	6	1	f	2026-05-14	12:30:00	Регулярная	\N		\N	\N
7	ORD-DEMO-MSK-07	Москва, Мясницкая улица, 24	Подтвержден производством	DEMO_MOSCOW_LOGISTICS	30250.00	2026-05-14 11:38:37.200035+03	2026-05-14 11:38:37.20004+03	7	1	f	2026-05-14	12:55:00	Разовая	\N		\N	\N
8	ORD-DEMO-MSK-08	Москва, Пятницкая улица, 25	В производстве	DEMO_MOSCOW_LOGISTICS	32000.00	2026-05-14 11:38:37.201707+03	2026-05-14 11:38:37.201711+03	8	1	f	2026-05-14	13:20:00	Регулярная	\N		\N	\N
9	ORD-DEMO-MSK-09	Москва, Земляной Вал, 33	Готов к отгрузке	DEMO_MOSCOW_LOGISTICS	33750.00	2026-05-14 11:38:37.203365+03	2026-05-14 11:38:37.203369+03	9	1	f	2026-05-14	13:45:00	Разовая	\N		\N	\N
10	ORD-DEMO-MSK-10	Москва, Пресненская набережная, 12	Отгружен	DEMO_MOSCOW_LOGISTICS	35500.00	2026-05-14 11:38:37.204558+03	2026-05-14 11:38:37.204563+03	10	1	f	2026-05-14	14:10:00	Регулярная	\N		\N	\N
\.


--
-- Data for Name: crm_orderitem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_orderitem (id, quantity, unit_price, line_total, supply_type, dish_id, ingredient_id, order_id, custom_tech_card_id, picked_quantity, item_status, item_comment, replacement_text) FROM stdin;
\.


--
-- Data for Name: crm_pickingsession; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_pickingsession (id, note, started_at, finished_at, updated_at, order_id, picker_id) FROM stdin;
\.


--
-- Data for Name: crm_productionreservation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_productionreservation (id, production_date, weight_kg, order_id) FROM stdin;
\.


--
-- Data for Name: crm_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_role (id, name) FROM stdin;
1	Менеджер
2	Логист
3	Сборщик заказов
4	Администратор системы
5	Курьер
\.


--
-- Data for Name: crm_route; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_route (id, planned_date, status, notes, logistician_id, max_duration_minutes, soft_limit_stops, strict_mode) FROM stdin;
1	2026-05-14	Выполняется	DEMO_MOSCOW_ROUTE_CENTER	2	360	5	f
2	2026-05-14	Опубликован	DEMO_MOSCOW_ROUTE_NORTH	2	360	5	f
3	2026-05-14	Опубликован	DEMO_MOSCOW_ROUTE_WEST	2	360	5	f
\.


--
-- Data for Name: crm_routestop; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_routestop (id, sequence_index, planned_time, actual_time, note, delivery_id, route_id, latitude, longitude, status, delivery_date, failure_reason, proof_of_delivery, proof_uploaded_at, proof_uploaded_by_id, service_time_minutes, proof_review_comment, proof_review_status, proof_reviewed_at, proof_reviewed_by_id) FROM stdin;
1	1	2026-05-14 13:45:00+03	\N	Центр Москвы: Красная площадь, дом 1	1	1	55.753930	37.620795	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
2	2	2026-05-14 14:10:00+03	\N	Центр Москвы: Тверская улица, дом 7	2	1	55.760186	37.609543	В пути	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
3	3	2026-05-14 14:35:00+03	\N	Центр Москвы: Большая Дмитровка, дом 11	6	1	55.762484	37.612799	В пути	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
4	1	2026-05-14 14:00:00+03	\N	Северный маршрут: Ленинградский проспект, дом 36	5	2	55.789742	37.557214	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
5	2	2026-05-14 14:25:00+03	\N	Северный маршрут: Мясницкая улица, дом 24	7	2	55.764799	37.637010	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
6	3	2026-05-14 14:50:00+03	\N	Северный маршрут: Земляной Вал, дом 33	9	2	55.757557	37.659548	Доставлено	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
7	1	2026-05-14 14:15:00+03	\N	Запад и деловой центр: Новый Арбат, дом 15	3	3	55.752815	37.592934	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
8	2	2026-05-14 14:40:00+03	\N	Запад и деловой центр: Кутузовский проспект, дом 2/1	4	3	55.749806	37.566734	Доставлено	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
9	3	2026-05-14 15:05:00+03	\N	Запад и деловой центр: Пятницкая улица, дом 25	8	3	55.740821	37.627093	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
10	4	2026-05-14 15:30:00+03	\N	Запад и деловой центр: Пресненская набережная, дом 12	10	3	55.749451	37.536924	Запланирована	2026-05-14			\N	\N	12		Ожидает проверки	\N	\N
\.


--
-- Data for Name: crm_techcard; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_techcard (id, version_label, description, photo_url, is_active, approved_by_id, dish_id) FROM stdin;
\.


--
-- Data for Name: crm_techcardcomponent; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_techcardcomponent (id, quantity, note, ingredient_id, tech_card_id) FROM stdin;
\.


--
-- Data for Name: crm_techcardvariant; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_techcardvariant (id, quantity, note, tech_card_id) FROM stdin;
\.


--
-- Data for Name: crm_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, full_name, phone) FROM stdin;
1	pbkdf2_sha256$1200000$i5mInn3g7wNxE5hFMlV3zr$ugUOGclY1xNoaoSfSdUJJYZrJVt63fDH7LDtnfeNh0Y=	\N	f	manager_demo			f	t	2026-05-14 11:38:36.329906+03	manager@art.com	Менеджер	
2	pbkdf2_sha256$1200000$FJDNSKR95f4PsmyAVuNYA8$QwytJv22tLukp32zj0no9l351ndmrSjUczEU3/lDwTA=	\N	f	logistic_demo			f	t	2026-05-14 11:38:36.533494+03	logistic@art.com	Логист	
3	pbkdf2_sha256$1200000$gC4kxvQZVLkZmJnQO0m0aj$wXNqRaQ+vcmjVXTiSzySceF39DAr/W+ld6tZL3gyrfc=	\N	f	picker_demo			f	t	2026-05-14 11:38:36.730839+03	picker@art.com	Сборщик заказов	
5	pbkdf2_sha256$1200000$oEebzcjq2s0WxSRDVQ3FjI$QSXCXWLN+LPY+Wu1Foe1yV3q/BtXUQonoOLchy51f+g=	\N	f	courier_demo			f	t	2026-05-14 11:38:37.208204+03	courier@art.com	Алексей Смирнов	
6	pbkdf2_sha256$1200000$5fE8eVraLVUqpnT4dNHgNj$h+aA6C6MXQDn6QCOGRGLYHDxgveJpQ99B1fjj3QKjiE=	\N	f	courier_demo_van			f	t	2026-05-14 11:38:37.406634+03	courier.van@art.com	Мария Волкова	
7	pbkdf2_sha256$1200000$cQuKUo8gsZS0XJMX0dBdfu$kCIgDywDCNHH574xQb8RcoCbelwlN0jy7+o+vdnTs1M=	\N	f	courier_demo_ref			f	t	2026-05-14 11:38:37.605428+03	courier.ref@art.com	Дмитрий Орлов	
4	pbkdf2_sha256$1200000$oQYTzwkuEUejDLqvEMMW5L$25iFu/qQhfbSpEfvc75TuXqs3NpBp2WL8jZ5HRnZj88=	2026-05-14 11:57:36.296005+03	f	admin_demo			f	t	2026-05-14 11:38:36.927295+03	admin@art.com	Администратор системы	
\.


--
-- Data for Name: crm_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: crm_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: crm_userrole; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crm_userrole (id, assigned_at, role_id, user_id) FROM stdin;
1	2026-05-14 11:38:36.530687+03	1	1
2	2026-05-14 11:38:36.728624+03	2	2
3	2026-05-14 11:38:36.92582+03	3	3
4	2026-05-14 11:38:37.122892+03	4	4
5	2026-05-14 11:38:37.403012+03	5	5
6	2026-05-14 11:38:37.602091+03	5	6
7	2026-05-14 11:38:37.799601+03	5	7
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	group
2	auth	permission
3	contenttypes	contenttype
4	sessions	session
5	crm	auditlog
6	crm	client
7	crm	clientallowedtechcard
8	crm	clientcontact
9	crm	clientstagehistory
10	crm	cooperationstage
11	crm	courier
12	crm	courierassignment
13	crm	delivery
14	crm	dish
15	crm	dishequipmentrequirement
16	crm	equipment
17	crm	equipmentreservation
18	crm	ingredient
19	crm	ingredientreservation
20	crm	ingredientstock
21	crm	interaction
22	crm	logisticianprofile
23	crm	order
24	crm	orderitem
25	crm	pickingsession
26	crm	productionreservation
27	crm	role
28	crm	route
29	crm	routestop
30	crm	techcard
31	crm	techcardcomponent
32	crm	techcardvariant
33	crm	user
34	crm	userrole
35	reports	report
36	admin_panel	backup
37	admin_panel	backupschedule
38	communications	directmessage
39	communications	entitycomment
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-05-14 11:38:22.003526+03
2	contenttypes	0002_remove_content_type_name	2026-05-14 11:38:22.008547+03
3	auth	0001_initial	2026-05-14 11:38:22.03731+03
4	auth	0002_alter_permission_name_max_length	2026-05-14 11:38:22.041793+03
5	auth	0003_alter_user_email_max_length	2026-05-14 11:38:22.045545+03
6	auth	0004_alter_user_username_opts	2026-05-14 11:38:22.049273+03
7	auth	0005_alter_user_last_login_null	2026-05-14 11:38:22.052434+03
8	auth	0006_require_contenttypes_0002	2026-05-14 11:38:22.05328+03
9	auth	0007_alter_validators_add_error_messages	2026-05-14 11:38:22.05658+03
10	auth	0008_alter_user_username_max_length	2026-05-14 11:38:22.059449+03
11	auth	0009_alter_user_last_name_max_length	2026-05-14 11:38:22.062759+03
12	auth	0010_alter_group_name_max_length	2026-05-14 11:38:22.067082+03
13	auth	0011_update_proxy_permissions	2026-05-14 11:38:22.069915+03
14	auth	0012_alter_user_first_name_max_length	2026-05-14 11:38:22.072889+03
15	crm	0001_initial	2026-05-14 11:38:22.370595+03
16	admin_panel	0001_initial	2026-05-14 11:38:22.395754+03
17	admin_panel	0002_backup_file_path_length	2026-05-14 11:38:22.406527+03
18	communications	0001_initial	2026-05-14 11:38:22.47737+03
19	crm	0002_client_current_stage	2026-05-14 11:38:22.494335+03
20	crm	0003_client_created_at	2026-05-14 11:38:22.505416+03
21	crm	0004_order_archived	2026-05-14 11:38:22.518042+03
22	crm	0005_delivery_fields	2026-05-14 11:38:22.558288+03
23	crm	0006_picking_session_and_item_fields	2026-05-14 11:38:22.617941+03
24	crm	0007_logistics_profile_and_cargo_fields	2026-05-14 11:38:22.765631+03
25	crm	0008_update_logistics_status_and_route_type	2026-05-14 11:38:22.819384+03
26	crm	0009_alter_logisticianprofile_id_alter_order_status	2026-05-14 11:38:22.841007+03
27	crm	0010_courier_current_latitude_courier_current_longitude_and_more	2026-05-14 11:38:22.923997+03
28	crm	0011_delivery_delivery_date_route_max_duration_minutes_and_more	2026-05-14 11:38:23.123773+03
29	crm	0012_routestop_proof_review_comment_and_more	2026-05-14 11:38:23.188645+03
30	crm	0013_equipment_client_daily_max_weight_kg_and_more	2026-05-14 11:38:23.568808+03
31	crm	0014_dish_default_price	2026-05-14 11:38:23.58562+03
32	crm	0015_dish_uom_fields	2026-05-14 11:38:23.647102+03
33	crm	0015_dish_daily_capacity	2026-05-14 11:38:23.665692+03
34	crm	0016_merge_0015_dish_daily_capacity_0015_dish_uom_fields	2026-05-14 11:38:23.666641+03
35	crm	0017_postgres_db_logic	2026-05-14 11:38:23.691152+03
36	reports	0001_initial	2026-05-14 11:38:23.722418+03
37	reports	0002_report_validation	2026-05-14 11:38:23.757781+03
38	sessions	0001_initial	2026-05-14 11:38:23.766673+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
muvy4fl8a0lu0lyokst0sspy53klpe8c	.eJxVjMEOwiAQRP-FsyFAoSwevfcbyMIuUjVtUtqT8d9tkx40mdO8N_MWEbe1xq3xEkcSV2HF5bdLmJ88HYAeON1nmedpXcYkD0WetMlhJn7dTvfvoGKr-zopJoKk2UHoM4CymjO73NEeBIud0QYUeO-Qs1IOje9CcVT6hCEU8fkC9aQ4PA:1wNRsu:Jr4n8w8H2kDJQKzp1U7G83VcHBcIRYYxfqzLQCixrfA	2026-05-28 11:57:36.317973+03
\.


--
-- Data for Name: reports_report; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reports_report (id, title, period_from, period_to, status, file, created_at, updated_at, created_by_id, validation_status, validation_message) FROM stdin;
1	Отчёт по продажам	2026-05-14	2026-05-14	ready		2026-05-14 11:38:37.843588+03	2026-05-14 11:38:37.843592+03	1	warn	
\.


--
-- Name: admin_panel_backup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_panel_backup_id_seq', 1, false);


--
-- Name: admin_panel_backupschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_panel_backupschedule_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 156, true);


--
-- Name: communications_directmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.communications_directmessage_id_seq', 1, false);


--
-- Name: communications_entitycomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.communications_entitycomment_id_seq', 1, false);


--
-- Name: crm_auditlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_auditlog_id_seq', 1, false);


--
-- Name: crm_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_client_id_seq', 10, true);


--
-- Name: crm_clientallowedtechcard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_clientallowedtechcard_id_seq', 1, false);


--
-- Name: crm_clientcontact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_clientcontact_id_seq', 1, false);


--
-- Name: crm_clientstagehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_clientstagehistory_id_seq', 10, true);


--
-- Name: crm_cooperationstage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_cooperationstage_id_seq', 4, true);


--
-- Name: crm_courier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_courier_id_seq', 3, true);


--
-- Name: crm_courierassignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_courierassignment_id_seq', 3, true);


--
-- Name: crm_delivery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_delivery_id_seq', 10, true);


--
-- Name: crm_dish_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_dish_id_seq', 1, false);


--
-- Name: crm_dishequipmentrequirement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_dishequipmentrequirement_id_seq', 1, false);


--
-- Name: crm_equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_equipment_id_seq', 1, false);


--
-- Name: crm_equipmentreservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_equipmentreservation_id_seq', 1, false);


--
-- Name: crm_ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_ingredient_id_seq', 1, false);


--
-- Name: crm_ingredientreservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_ingredientreservation_id_seq', 1, false);


--
-- Name: crm_ingredientstock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_ingredientstock_id_seq', 1, false);


--
-- Name: crm_interaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_interaction_id_seq', 10, true);


--
-- Name: crm_logisticianprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_logisticianprofile_id_seq', 1, true);


--
-- Name: crm_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_order_id_seq', 10, true);


--
-- Name: crm_orderitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_orderitem_id_seq', 1, false);


--
-- Name: crm_pickingsession_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_pickingsession_id_seq', 1, false);


--
-- Name: crm_productionreservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_productionreservation_id_seq', 1, false);


--
-- Name: crm_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_role_id_seq', 5, true);


--
-- Name: crm_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_route_id_seq', 3, true);


--
-- Name: crm_routestop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_routestop_id_seq', 10, true);


--
-- Name: crm_techcard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_techcard_id_seq', 1, false);


--
-- Name: crm_techcardcomponent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_techcardcomponent_id_seq', 1, false);


--
-- Name: crm_techcardvariant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_techcardvariant_id_seq', 1, false);


--
-- Name: crm_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_user_groups_id_seq', 1, false);


--
-- Name: crm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_user_id_seq', 7, true);


--
-- Name: crm_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_user_user_permissions_id_seq', 1, false);


--
-- Name: crm_userrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crm_userrole_id_seq', 7, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 39, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 38, true);


--
-- Name: reports_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reports_report_id_seq', 1, true);


--
-- Name: admin_panel_backup admin_panel_backup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_panel_backup
    ADD CONSTRAINT admin_panel_backup_pkey PRIMARY KEY (id);


--
-- Name: admin_panel_backupschedule admin_panel_backupschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_panel_backupschedule
    ADD CONSTRAINT admin_panel_backupschedule_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: communications_directmessage communications_directmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_directmessage
    ADD CONSTRAINT communications_directmessage_pkey PRIMARY KEY (id);


--
-- Name: communications_entitycomment communications_entitycomment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_entitycomment
    ADD CONSTRAINT communications_entitycomment_pkey PRIMARY KEY (id);


--
-- Name: crm_auditlog crm_auditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_auditlog
    ADD CONSTRAINT crm_auditlog_pkey PRIMARY KEY (id);


--
-- Name: crm_client crm_client_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_client
    ADD CONSTRAINT crm_client_pkey PRIMARY KEY (id);


--
-- Name: crm_clientallowedtechcard crm_clientallowedtechcard_client_id_tech_card_id_f1bfd130_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientallowedtechcard
    ADD CONSTRAINT crm_clientallowedtechcard_client_id_tech_card_id_f1bfd130_uniq UNIQUE (client_id, tech_card_id);


--
-- Name: crm_clientallowedtechcard crm_clientallowedtechcard_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientallowedtechcard
    ADD CONSTRAINT crm_clientallowedtechcard_pkey PRIMARY KEY (id);


--
-- Name: crm_clientcontact crm_clientcontact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientcontact
    ADD CONSTRAINT crm_clientcontact_pkey PRIMARY KEY (id);


--
-- Name: crm_clientstagehistory crm_clientstagehistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientstagehistory
    ADD CONSTRAINT crm_clientstagehistory_pkey PRIMARY KEY (id);


--
-- Name: crm_cooperationstage crm_cooperationstage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_cooperationstage
    ADD CONSTRAINT crm_cooperationstage_pkey PRIMARY KEY (id);


--
-- Name: crm_courier crm_courier_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courier
    ADD CONSTRAINT crm_courier_pkey PRIMARY KEY (id);


--
-- Name: crm_courier crm_courier_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courier
    ADD CONSTRAINT crm_courier_user_id_key UNIQUE (user_id);


--
-- Name: crm_courierassignment crm_courierassignment_courier_id_route_id_4ca14639_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courierassignment
    ADD CONSTRAINT crm_courierassignment_courier_id_route_id_4ca14639_uniq UNIQUE (courier_id, route_id);


--
-- Name: crm_courierassignment crm_courierassignment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courierassignment
    ADD CONSTRAINT crm_courierassignment_pkey PRIMARY KEY (id);


--
-- Name: crm_delivery crm_delivery_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_delivery
    ADD CONSTRAINT crm_delivery_pkey PRIMARY KEY (id);


--
-- Name: crm_dish crm_dish_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dish
    ADD CONSTRAINT crm_dish_pkey PRIMARY KEY (id);


--
-- Name: crm_dishequipmentrequirement crm_dishequipmentrequirement_dish_id_equipment_id_03d5c14f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dishequipmentrequirement
    ADD CONSTRAINT crm_dishequipmentrequirement_dish_id_equipment_id_03d5c14f_uniq UNIQUE (dish_id, equipment_id);


--
-- Name: crm_dishequipmentrequirement crm_dishequipmentrequirement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dishequipmentrequirement
    ADD CONSTRAINT crm_dishequipmentrequirement_pkey PRIMARY KEY (id);


--
-- Name: crm_equipment crm_equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_equipment
    ADD CONSTRAINT crm_equipment_pkey PRIMARY KEY (id);


--
-- Name: crm_equipmentreservation crm_equipmentreservation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_equipmentreservation
    ADD CONSTRAINT crm_equipmentreservation_pkey PRIMARY KEY (id);


--
-- Name: crm_ingredient crm_ingredient_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredient
    ADD CONSTRAINT crm_ingredient_name_key UNIQUE (name);


--
-- Name: crm_ingredient crm_ingredient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredient
    ADD CONSTRAINT crm_ingredient_pkey PRIMARY KEY (id);


--
-- Name: crm_ingredientreservation crm_ingredientreservation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientreservation
    ADD CONSTRAINT crm_ingredientreservation_pkey PRIMARY KEY (id);


--
-- Name: crm_ingredientstock crm_ingredientstock_ingredient_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientstock
    ADD CONSTRAINT crm_ingredientstock_ingredient_id_key UNIQUE (ingredient_id);


--
-- Name: crm_ingredientstock crm_ingredientstock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientstock
    ADD CONSTRAINT crm_ingredientstock_pkey PRIMARY KEY (id);


--
-- Name: crm_interaction crm_interaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_interaction
    ADD CONSTRAINT crm_interaction_pkey PRIMARY KEY (id);


--
-- Name: crm_logisticianprofile crm_logisticianprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_logisticianprofile
    ADD CONSTRAINT crm_logisticianprofile_pkey PRIMARY KEY (id);


--
-- Name: crm_logisticianprofile crm_logisticianprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_logisticianprofile
    ADD CONSTRAINT crm_logisticianprofile_user_id_key UNIQUE (user_id);


--
-- Name: crm_order crm_order_order_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_order
    ADD CONSTRAINT crm_order_order_number_key UNIQUE (order_number);


--
-- Name: crm_order crm_order_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_order
    ADD CONSTRAINT crm_order_pkey PRIMARY KEY (id);


--
-- Name: crm_orderitem crm_orderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_orderitem
    ADD CONSTRAINT crm_orderitem_pkey PRIMARY KEY (id);


--
-- Name: crm_pickingsession crm_pickingsession_order_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_pickingsession
    ADD CONSTRAINT crm_pickingsession_order_id_key UNIQUE (order_id);


--
-- Name: crm_pickingsession crm_pickingsession_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_pickingsession
    ADD CONSTRAINT crm_pickingsession_pkey PRIMARY KEY (id);


--
-- Name: crm_productionreservation crm_productionreservation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_productionreservation
    ADD CONSTRAINT crm_productionreservation_pkey PRIMARY KEY (id);


--
-- Name: crm_role crm_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_role
    ADD CONSTRAINT crm_role_name_key UNIQUE (name);


--
-- Name: crm_role crm_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_role
    ADD CONSTRAINT crm_role_pkey PRIMARY KEY (id);


--
-- Name: crm_route crm_route_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_route
    ADD CONSTRAINT crm_route_pkey PRIMARY KEY (id);


--
-- Name: crm_routestop crm_routestop_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_routestop
    ADD CONSTRAINT crm_routestop_pkey PRIMARY KEY (id);


--
-- Name: crm_techcard crm_techcard_dish_id_version_label_b05cfe34_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcard
    ADD CONSTRAINT crm_techcard_dish_id_version_label_b05cfe34_uniq UNIQUE (dish_id, version_label);


--
-- Name: crm_techcard crm_techcard_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcard
    ADD CONSTRAINT crm_techcard_pkey PRIMARY KEY (id);


--
-- Name: crm_techcardcomponent crm_techcardcomponent_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcardcomponent
    ADD CONSTRAINT crm_techcardcomponent_pkey PRIMARY KEY (id);


--
-- Name: crm_techcardvariant crm_techcardvariant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcardvariant
    ADD CONSTRAINT crm_techcardvariant_pkey PRIMARY KEY (id);


--
-- Name: crm_user crm_user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user
    ADD CONSTRAINT crm_user_email_key UNIQUE (email);


--
-- Name: crm_user_groups crm_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_groups
    ADD CONSTRAINT crm_user_groups_pkey PRIMARY KEY (id);


--
-- Name: crm_user_groups crm_user_groups_user_id_group_id_56d4cc88_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_groups
    ADD CONSTRAINT crm_user_groups_user_id_group_id_56d4cc88_uniq UNIQUE (user_id, group_id);


--
-- Name: crm_user crm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user
    ADD CONSTRAINT crm_user_pkey PRIMARY KEY (id);


--
-- Name: crm_user_user_permissions crm_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_user_permissions
    ADD CONSTRAINT crm_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: crm_user_user_permissions crm_user_user_permissions_user_id_permission_id_72b1e4e1_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_user_permissions
    ADD CONSTRAINT crm_user_user_permissions_user_id_permission_id_72b1e4e1_uniq UNIQUE (user_id, permission_id);


--
-- Name: crm_user crm_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user
    ADD CONSTRAINT crm_user_username_key UNIQUE (username);


--
-- Name: crm_userrole crm_userrole_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_userrole
    ADD CONSTRAINT crm_userrole_pkey PRIMARY KEY (id);


--
-- Name: crm_userrole crm_userrole_user_id_role_id_fa7b18da_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_userrole
    ADD CONSTRAINT crm_userrole_user_id_role_id_fa7b18da_uniq UNIQUE (user_id, role_id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: reports_report reports_report_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reports_report
    ADD CONSTRAINT reports_report_pkey PRIMARY KEY (id);


--
-- Name: admin_panel_backup_created_by_id_f9e87668; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_panel_backup_created_by_id_f9e87668 ON public.admin_panel_backup USING btree (created_by_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: communicati_content_67dfbc_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communicati_content_67dfbc_idx ON public.communications_entitycomment USING btree (content_type_id, object_id, created_at);


--
-- Name: communicati_recipie_c7ddb4_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communicati_recipie_c7ddb4_idx ON public.communications_directmessage USING btree (recipient_id, read_at, created_at);


--
-- Name: communicati_sender__0f8c80_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communicati_sender__0f8c80_idx ON public.communications_directmessage USING btree (sender_id, recipient_id, created_at);


--
-- Name: communications_directmessage_recipient_id_267e91bf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communications_directmessage_recipient_id_267e91bf ON public.communications_directmessage USING btree (recipient_id);


--
-- Name: communications_directmessage_sender_id_5355d0f2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communications_directmessage_sender_id_5355d0f2 ON public.communications_directmessage USING btree (sender_id);


--
-- Name: communications_entitycomment_author_id_b58bd8f7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communications_entitycomment_author_id_b58bd8f7 ON public.communications_entitycomment USING btree (author_id);


--
-- Name: communications_entitycomment_content_type_id_71d2a881; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX communications_entitycomment_content_type_id_71d2a881 ON public.communications_entitycomment USING btree (content_type_id);


--
-- Name: crm_auditlog_actor_id_4382924f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_auditlog_actor_id_4382924f ON public.crm_auditlog USING btree (actor_id);


--
-- Name: crm_client_current_stage_id_e8a55701; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_client_current_stage_id_e8a55701 ON public.crm_client USING btree (current_stage_id);


--
-- Name: crm_client_responsible_manager_id_7081e9b4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_client_responsible_manager_id_7081e9b4 ON public.crm_client USING btree (responsible_manager_id);


--
-- Name: crm_clientallowedtechcard_client_id_a202bbc1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientallowedtechcard_client_id_a202bbc1 ON public.crm_clientallowedtechcard USING btree (client_id);


--
-- Name: crm_clientallowedtechcard_tech_card_id_4956fc6d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientallowedtechcard_tech_card_id_4956fc6d ON public.crm_clientallowedtechcard USING btree (tech_card_id);


--
-- Name: crm_clientcontact_client_id_b44e105e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientcontact_client_id_b44e105e ON public.crm_clientcontact USING btree (client_id);


--
-- Name: crm_clientstagehistory_changed_by_id_84f6d086; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientstagehistory_changed_by_id_84f6d086 ON public.crm_clientstagehistory USING btree (changed_by_id);


--
-- Name: crm_clientstagehistory_client_id_926d0169; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientstagehistory_client_id_926d0169 ON public.crm_clientstagehistory USING btree (client_id);


--
-- Name: crm_clientstagehistory_stage_id_04e1997a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_clientstagehistory_stage_id_04e1997a ON public.crm_clientstagehistory USING btree (stage_id);


--
-- Name: crm_courierassignment_courier_id_d66fb584; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_courierassignment_courier_id_d66fb584 ON public.crm_courierassignment USING btree (courier_id);


--
-- Name: crm_courierassignment_route_id_40d05eac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_courierassignment_route_id_40d05eac ON public.crm_courierassignment USING btree (route_id);


--
-- Name: crm_delivery_courier_id_fa676b65; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_delivery_courier_id_fa676b65 ON public.crm_delivery USING btree (courier_id);


--
-- Name: crm_delivery_order_id_88ce6731; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_delivery_order_id_88ce6731 ON public.crm_delivery USING btree (order_id);


--
-- Name: crm_delivery_route_id_7a215b73; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_delivery_route_id_7a215b73 ON public.crm_delivery USING btree (route_id);


--
-- Name: crm_dish_created_by_id_1ec5aa20; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_dish_created_by_id_1ec5aa20 ON public.crm_dish USING btree (created_by_id);


--
-- Name: crm_dishequipmentrequirement_dish_id_d09c1cdf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_dishequipmentrequirement_dish_id_d09c1cdf ON public.crm_dishequipmentrequirement USING btree (dish_id);


--
-- Name: crm_dishequipmentrequirement_equipment_id_c03741cd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_dishequipmentrequirement_equipment_id_c03741cd ON public.crm_dishequipmentrequirement USING btree (equipment_id);


--
-- Name: crm_equipmentreservation_equipment_id_01460725; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_equipmentreservation_equipment_id_01460725 ON public.crm_equipmentreservation USING btree (equipment_id);


--
-- Name: crm_equipmentreservation_order_id_e9f68c20; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_equipmentreservation_order_id_e9f68c20 ON public.crm_equipmentreservation USING btree (order_id);


--
-- Name: crm_ingredient_name_cd2f75d5_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_ingredient_name_cd2f75d5_like ON public.crm_ingredient USING btree (name varchar_pattern_ops);


--
-- Name: crm_ingredientreservation_ingredient_id_a8564254; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_ingredientreservation_ingredient_id_a8564254 ON public.crm_ingredientreservation USING btree (ingredient_id);


--
-- Name: crm_ingredientreservation_order_id_17138f75; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_ingredientreservation_order_id_17138f75 ON public.crm_ingredientreservation USING btree (order_id);


--
-- Name: crm_interaction_client_id_e63a8170; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_interaction_client_id_e63a8170 ON public.crm_interaction USING btree (client_id);


--
-- Name: crm_interaction_manager_id_24afb2b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_interaction_manager_id_24afb2b9 ON public.crm_interaction USING btree (manager_id);


--
-- Name: crm_order_client_id_8ed70023; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_order_client_id_8ed70023 ON public.crm_order USING btree (client_id);


--
-- Name: crm_order_manager_id_039a402f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_order_manager_id_039a402f ON public.crm_order USING btree (manager_id);


--
-- Name: crm_order_order_number_16e6bd13_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_order_order_number_16e6bd13_like ON public.crm_order USING btree (order_number varchar_pattern_ops);


--
-- Name: crm_orderitem_custom_tech_card_id_5e4ea50e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_orderitem_custom_tech_card_id_5e4ea50e ON public.crm_orderitem USING btree (custom_tech_card_id);


--
-- Name: crm_orderitem_dish_id_e3114b2a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_orderitem_dish_id_e3114b2a ON public.crm_orderitem USING btree (dish_id);


--
-- Name: crm_orderitem_ingredient_id_2185a1eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_orderitem_ingredient_id_2185a1eb ON public.crm_orderitem USING btree (ingredient_id);


--
-- Name: crm_orderitem_order_id_7ec9f773; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_orderitem_order_id_7ec9f773 ON public.crm_orderitem USING btree (order_id);


--
-- Name: crm_pickingsession_picker_id_ee342393; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_pickingsession_picker_id_ee342393 ON public.crm_pickingsession USING btree (picker_id);


--
-- Name: crm_productionreservation_order_id_4efb72f7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_productionreservation_order_id_4efb72f7 ON public.crm_productionreservation USING btree (order_id);


--
-- Name: crm_role_name_9490777a_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_role_name_9490777a_like ON public.crm_role USING btree (name varchar_pattern_ops);


--
-- Name: crm_route_logistician_id_a5ae8d10; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_route_logistician_id_a5ae8d10 ON public.crm_route USING btree (logistician_id);


--
-- Name: crm_routestop_delivery_id_c0c90c7b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_routestop_delivery_id_c0c90c7b ON public.crm_routestop USING btree (delivery_id);


--
-- Name: crm_routestop_proof_reviewed_by_id_27311351; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_routestop_proof_reviewed_by_id_27311351 ON public.crm_routestop USING btree (proof_reviewed_by_id);


--
-- Name: crm_routestop_proof_uploaded_by_id_13f26b97; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_routestop_proof_uploaded_by_id_13f26b97 ON public.crm_routestop USING btree (proof_uploaded_by_id);


--
-- Name: crm_routestop_route_id_38bf345b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_routestop_route_id_38bf345b ON public.crm_routestop USING btree (route_id);


--
-- Name: crm_techcard_approved_by_id_32ef922d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_techcard_approved_by_id_32ef922d ON public.crm_techcard USING btree (approved_by_id);


--
-- Name: crm_techcard_dish_id_277af818; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_techcard_dish_id_277af818 ON public.crm_techcard USING btree (dish_id);


--
-- Name: crm_techcardcomponent_ingredient_id_4ce9ea00; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_techcardcomponent_ingredient_id_4ce9ea00 ON public.crm_techcardcomponent USING btree (ingredient_id);


--
-- Name: crm_techcardcomponent_tech_card_id_623c4128; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_techcardcomponent_tech_card_id_623c4128 ON public.crm_techcardcomponent USING btree (tech_card_id);


--
-- Name: crm_techcardvariant_tech_card_id_43f7c6d6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_techcardvariant_tech_card_id_43f7c6d6 ON public.crm_techcardvariant USING btree (tech_card_id);


--
-- Name: crm_user_email_3827a8fd_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_email_3827a8fd_like ON public.crm_user USING btree (email varchar_pattern_ops);


--
-- Name: crm_user_groups_group_id_93d3047c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_groups_group_id_93d3047c ON public.crm_user_groups USING btree (group_id);


--
-- Name: crm_user_groups_user_id_5847c7a0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_groups_user_id_5847c7a0 ON public.crm_user_groups USING btree (user_id);


--
-- Name: crm_user_user_permissions_permission_id_0f701f96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_user_permissions_permission_id_0f701f96 ON public.crm_user_user_permissions USING btree (permission_id);


--
-- Name: crm_user_user_permissions_user_id_047208b5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_user_permissions_user_id_047208b5 ON public.crm_user_user_permissions USING btree (user_id);


--
-- Name: crm_user_username_1ca997f7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_user_username_1ca997f7_like ON public.crm_user USING btree (username varchar_pattern_ops);


--
-- Name: crm_userrole_role_id_764fcdba; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_userrole_role_id_764fcdba ON public.crm_userrole USING btree (role_id);


--
-- Name: crm_userrole_user_id_e281baa8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX crm_userrole_user_id_e281baa8 ON public.crm_userrole USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: reports_report_created_by_id_e9adac24; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reports_report_created_by_id_e9adac24 ON public.reports_report USING btree (created_by_id);


--
-- Name: crm_ingredientreservation trg_crm_ingredientreservation_check; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_crm_ingredientreservation_check BEFORE INSERT OR UPDATE OF quantity, ingredient_id, production_date ON public.crm_ingredientreservation FOR EACH ROW EXECUTE FUNCTION public.crm_tg_check_ingredient_reservation();


--
-- Name: crm_order trg_crm_order_validate_delivery_date; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_crm_order_validate_delivery_date BEFORE INSERT OR UPDATE OF delivery_date ON public.crm_order FOR EACH ROW EXECUTE FUNCTION public.crm_tg_validate_delivery_date();


--
-- Name: crm_orderitem trg_crm_orderitem_prepare; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_crm_orderitem_prepare BEFORE INSERT OR UPDATE OF quantity, unit_price ON public.crm_orderitem FOR EACH ROW EXECUTE FUNCTION public.crm_tg_prepare_orderitem();


--
-- Name: crm_orderitem trg_crm_orderitem_total_recalc; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_crm_orderitem_total_recalc AFTER INSERT OR DELETE OR UPDATE ON public.crm_orderitem FOR EACH ROW EXECUTE FUNCTION public.crm_tg_orderitem_total_recalc();


--
-- Name: admin_panel_backup admin_panel_backup_created_by_id_f9e87668_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_panel_backup
    ADD CONSTRAINT admin_panel_backup_created_by_id_f9e87668_fk_crm_user_id FOREIGN KEY (created_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: communications_directmessage communications_direc_recipient_id_267e91bf_fk_crm_user_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_directmessage
    ADD CONSTRAINT communications_direc_recipient_id_267e91bf_fk_crm_user_ FOREIGN KEY (recipient_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: communications_directmessage communications_directmessage_sender_id_5355d0f2_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_directmessage
    ADD CONSTRAINT communications_directmessage_sender_id_5355d0f2_fk_crm_user_id FOREIGN KEY (sender_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: communications_entitycomment communications_entit_content_type_id_71d2a881_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_entitycomment
    ADD CONSTRAINT communications_entit_content_type_id_71d2a881_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: communications_entitycomment communications_entitycomment_author_id_b58bd8f7_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communications_entitycomment
    ADD CONSTRAINT communications_entitycomment_author_id_b58bd8f7_fk_crm_user_id FOREIGN KEY (author_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_auditlog crm_auditlog_actor_id_4382924f_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_auditlog
    ADD CONSTRAINT crm_auditlog_actor_id_4382924f_fk_crm_user_id FOREIGN KEY (actor_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_client crm_client_current_stage_id_e8a55701_fk_crm_cooperationstage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_client
    ADD CONSTRAINT crm_client_current_stage_id_e8a55701_fk_crm_cooperationstage_id FOREIGN KEY (current_stage_id) REFERENCES public.crm_cooperationstage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_client crm_client_responsible_manager_id_7081e9b4_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_client
    ADD CONSTRAINT crm_client_responsible_manager_id_7081e9b4_fk_crm_user_id FOREIGN KEY (responsible_manager_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientallowedtechcard crm_clientallowedtec_tech_card_id_4956fc6d_fk_crm_techc; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientallowedtechcard
    ADD CONSTRAINT crm_clientallowedtec_tech_card_id_4956fc6d_fk_crm_techc FOREIGN KEY (tech_card_id) REFERENCES public.crm_techcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientallowedtechcard crm_clientallowedtechcard_client_id_a202bbc1_fk_crm_client_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientallowedtechcard
    ADD CONSTRAINT crm_clientallowedtechcard_client_id_a202bbc1_fk_crm_client_id FOREIGN KEY (client_id) REFERENCES public.crm_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientcontact crm_clientcontact_client_id_b44e105e_fk_crm_client_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientcontact
    ADD CONSTRAINT crm_clientcontact_client_id_b44e105e_fk_crm_client_id FOREIGN KEY (client_id) REFERENCES public.crm_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientstagehistory crm_clientstagehisto_stage_id_04e1997a_fk_crm_coope; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientstagehistory
    ADD CONSTRAINT crm_clientstagehisto_stage_id_04e1997a_fk_crm_coope FOREIGN KEY (stage_id) REFERENCES public.crm_cooperationstage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientstagehistory crm_clientstagehistory_changed_by_id_84f6d086_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientstagehistory
    ADD CONSTRAINT crm_clientstagehistory_changed_by_id_84f6d086_fk_crm_user_id FOREIGN KEY (changed_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_clientstagehistory crm_clientstagehistory_client_id_926d0169_fk_crm_client_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_clientstagehistory
    ADD CONSTRAINT crm_clientstagehistory_client_id_926d0169_fk_crm_client_id FOREIGN KEY (client_id) REFERENCES public.crm_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_courier crm_courier_user_id_2f7f2458_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courier
    ADD CONSTRAINT crm_courier_user_id_2f7f2458_fk_crm_user_id FOREIGN KEY (user_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_courierassignment crm_courierassignment_courier_id_d66fb584_fk_crm_courier_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courierassignment
    ADD CONSTRAINT crm_courierassignment_courier_id_d66fb584_fk_crm_courier_id FOREIGN KEY (courier_id) REFERENCES public.crm_courier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_courierassignment crm_courierassignment_route_id_40d05eac_fk_crm_route_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_courierassignment
    ADD CONSTRAINT crm_courierassignment_route_id_40d05eac_fk_crm_route_id FOREIGN KEY (route_id) REFERENCES public.crm_route(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_delivery crm_delivery_courier_id_fa676b65_fk_crm_courier_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_delivery
    ADD CONSTRAINT crm_delivery_courier_id_fa676b65_fk_crm_courier_id FOREIGN KEY (courier_id) REFERENCES public.crm_courier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_delivery crm_delivery_order_id_88ce6731_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_delivery
    ADD CONSTRAINT crm_delivery_order_id_88ce6731_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_delivery crm_delivery_route_id_7a215b73_fk_crm_route_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_delivery
    ADD CONSTRAINT crm_delivery_route_id_7a215b73_fk_crm_route_id FOREIGN KEY (route_id) REFERENCES public.crm_route(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_dish crm_dish_created_by_id_1ec5aa20_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dish
    ADD CONSTRAINT crm_dish_created_by_id_1ec5aa20_fk_crm_user_id FOREIGN KEY (created_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_dishequipmentrequirement crm_dishequipmentreq_equipment_id_c03741cd_fk_crm_equip; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dishequipmentrequirement
    ADD CONSTRAINT crm_dishequipmentreq_equipment_id_c03741cd_fk_crm_equip FOREIGN KEY (equipment_id) REFERENCES public.crm_equipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_dishequipmentrequirement crm_dishequipmentrequirement_dish_id_d09c1cdf_fk_crm_dish_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_dishequipmentrequirement
    ADD CONSTRAINT crm_dishequipmentrequirement_dish_id_d09c1cdf_fk_crm_dish_id FOREIGN KEY (dish_id) REFERENCES public.crm_dish(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_equipmentreservation crm_equipmentreserva_equipment_id_01460725_fk_crm_equip; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_equipmentreservation
    ADD CONSTRAINT crm_equipmentreserva_equipment_id_01460725_fk_crm_equip FOREIGN KEY (equipment_id) REFERENCES public.crm_equipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_equipmentreservation crm_equipmentreservation_order_id_e9f68c20_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_equipmentreservation
    ADD CONSTRAINT crm_equipmentreservation_order_id_e9f68c20_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_ingredientreservation crm_ingredientreserv_ingredient_id_a8564254_fk_crm_ingre; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientreservation
    ADD CONSTRAINT crm_ingredientreserv_ingredient_id_a8564254_fk_crm_ingre FOREIGN KEY (ingredient_id) REFERENCES public.crm_ingredient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_ingredientreservation crm_ingredientreservation_order_id_17138f75_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientreservation
    ADD CONSTRAINT crm_ingredientreservation_order_id_17138f75_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_ingredientstock crm_ingredientstock_ingredient_id_8f0c8b74_fk_crm_ingredient_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_ingredientstock
    ADD CONSTRAINT crm_ingredientstock_ingredient_id_8f0c8b74_fk_crm_ingredient_id FOREIGN KEY (ingredient_id) REFERENCES public.crm_ingredient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_interaction crm_interaction_client_id_e63a8170_fk_crm_client_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_interaction
    ADD CONSTRAINT crm_interaction_client_id_e63a8170_fk_crm_client_id FOREIGN KEY (client_id) REFERENCES public.crm_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_interaction crm_interaction_manager_id_24afb2b9_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_interaction
    ADD CONSTRAINT crm_interaction_manager_id_24afb2b9_fk_crm_user_id FOREIGN KEY (manager_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_logisticianprofile crm_logisticianprofile_user_id_734435f2_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_logisticianprofile
    ADD CONSTRAINT crm_logisticianprofile_user_id_734435f2_fk_crm_user_id FOREIGN KEY (user_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_order crm_order_client_id_8ed70023_fk_crm_client_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_order
    ADD CONSTRAINT crm_order_client_id_8ed70023_fk_crm_client_id FOREIGN KEY (client_id) REFERENCES public.crm_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_order crm_order_manager_id_039a402f_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_order
    ADD CONSTRAINT crm_order_manager_id_039a402f_fk_crm_user_id FOREIGN KEY (manager_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_orderitem crm_orderitem_custom_tech_card_id_5e4ea50e_fk_crm_techcard_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_orderitem
    ADD CONSTRAINT crm_orderitem_custom_tech_card_id_5e4ea50e_fk_crm_techcard_id FOREIGN KEY (custom_tech_card_id) REFERENCES public.crm_techcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_orderitem crm_orderitem_dish_id_e3114b2a_fk_crm_dish_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_orderitem
    ADD CONSTRAINT crm_orderitem_dish_id_e3114b2a_fk_crm_dish_id FOREIGN KEY (dish_id) REFERENCES public.crm_dish(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_orderitem crm_orderitem_ingredient_id_2185a1eb_fk_crm_ingredient_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_orderitem
    ADD CONSTRAINT crm_orderitem_ingredient_id_2185a1eb_fk_crm_ingredient_id FOREIGN KEY (ingredient_id) REFERENCES public.crm_ingredient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_orderitem crm_orderitem_order_id_7ec9f773_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_orderitem
    ADD CONSTRAINT crm_orderitem_order_id_7ec9f773_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_pickingsession crm_pickingsession_order_id_3b52eab3_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_pickingsession
    ADD CONSTRAINT crm_pickingsession_order_id_3b52eab3_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_pickingsession crm_pickingsession_picker_id_ee342393_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_pickingsession
    ADD CONSTRAINT crm_pickingsession_picker_id_ee342393_fk_crm_user_id FOREIGN KEY (picker_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_productionreservation crm_productionreservation_order_id_4efb72f7_fk_crm_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_productionreservation
    ADD CONSTRAINT crm_productionreservation_order_id_4efb72f7_fk_crm_order_id FOREIGN KEY (order_id) REFERENCES public.crm_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_route crm_route_logistician_id_a5ae8d10_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_route
    ADD CONSTRAINT crm_route_logistician_id_a5ae8d10_fk_crm_user_id FOREIGN KEY (logistician_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_routestop crm_routestop_delivery_id_c0c90c7b_fk_crm_delivery_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_routestop
    ADD CONSTRAINT crm_routestop_delivery_id_c0c90c7b_fk_crm_delivery_id FOREIGN KEY (delivery_id) REFERENCES public.crm_delivery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_routestop crm_routestop_proof_reviewed_by_id_27311351_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_routestop
    ADD CONSTRAINT crm_routestop_proof_reviewed_by_id_27311351_fk_crm_user_id FOREIGN KEY (proof_reviewed_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_routestop crm_routestop_proof_uploaded_by_id_13f26b97_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_routestop
    ADD CONSTRAINT crm_routestop_proof_uploaded_by_id_13f26b97_fk_crm_user_id FOREIGN KEY (proof_uploaded_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_routestop crm_routestop_route_id_38bf345b_fk_crm_route_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_routestop
    ADD CONSTRAINT crm_routestop_route_id_38bf345b_fk_crm_route_id FOREIGN KEY (route_id) REFERENCES public.crm_route(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_techcard crm_techcard_approved_by_id_32ef922d_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcard
    ADD CONSTRAINT crm_techcard_approved_by_id_32ef922d_fk_crm_user_id FOREIGN KEY (approved_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_techcard crm_techcard_dish_id_277af818_fk_crm_dish_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcard
    ADD CONSTRAINT crm_techcard_dish_id_277af818_fk_crm_dish_id FOREIGN KEY (dish_id) REFERENCES public.crm_dish(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_techcardcomponent crm_techcardcomponen_ingredient_id_4ce9ea00_fk_crm_ingre; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcardcomponent
    ADD CONSTRAINT crm_techcardcomponen_ingredient_id_4ce9ea00_fk_crm_ingre FOREIGN KEY (ingredient_id) REFERENCES public.crm_ingredient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_techcardcomponent crm_techcardcomponent_tech_card_id_623c4128_fk_crm_techcard_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcardcomponent
    ADD CONSTRAINT crm_techcardcomponent_tech_card_id_623c4128_fk_crm_techcard_id FOREIGN KEY (tech_card_id) REFERENCES public.crm_techcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_techcardvariant crm_techcardvariant_tech_card_id_43f7c6d6_fk_crm_techcard_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_techcardvariant
    ADD CONSTRAINT crm_techcardvariant_tech_card_id_43f7c6d6_fk_crm_techcard_id FOREIGN KEY (tech_card_id) REFERENCES public.crm_techcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_user_groups crm_user_groups_group_id_93d3047c_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_groups
    ADD CONSTRAINT crm_user_groups_group_id_93d3047c_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_user_groups crm_user_groups_user_id_5847c7a0_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_groups
    ADD CONSTRAINT crm_user_groups_user_id_5847c7a0_fk_crm_user_id FOREIGN KEY (user_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_user_user_permissions crm_user_user_permis_permission_id_0f701f96_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_user_permissions
    ADD CONSTRAINT crm_user_user_permis_permission_id_0f701f96_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_user_user_permissions crm_user_user_permissions_user_id_047208b5_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_user_user_permissions
    ADD CONSTRAINT crm_user_user_permissions_user_id_047208b5_fk_crm_user_id FOREIGN KEY (user_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_userrole crm_userrole_role_id_764fcdba_fk_crm_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_userrole
    ADD CONSTRAINT crm_userrole_role_id_764fcdba_fk_crm_role_id FOREIGN KEY (role_id) REFERENCES public.crm_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crm_userrole crm_userrole_user_id_e281baa8_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crm_userrole
    ADD CONSTRAINT crm_userrole_user_id_e281baa8_fk_crm_user_id FOREIGN KEY (user_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_report reports_report_created_by_id_e9adac24_fk_crm_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reports_report
    ADD CONSTRAINT reports_report_created_by_id_e9adac24_fk_crm_user_id FOREIGN KEY (created_by_id) REFERENCES public.crm_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict A6mucbCYoRc1fMwXeGccmOkxP6nr1fUNByQkem0AtSaDN1IcU403Jk20LAQSy69

