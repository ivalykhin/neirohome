BEGIN;
--
-- Create model DataSets
--
CREATE TABLE `prediction_research_datasets` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `data_set_on_date` date NOT NULL, `input_data` varchar(512) NOT NULL, `output_data` numeric(8, 4) NOT NULL, `creation_date` datetime NOT NULL);
--
-- Create model NeiroNet
--
CREATE TABLE `prediction_research_neironet` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(256) NOT NULL, `number_of_inputs` integer NOT NULL, `number_of_outputs` integer NOT NULL, `training_epochs` integer NOT NULL, `creation_date` datetime NOT NULL, `neironet_file` varchar(512) NULL, `description`longtext NULL);
--
-- Create model Prediction
--
CREATE TABLE `prediction_research_prediction` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `number_of_inputs` integer NOT NULL, `number_of_outputs` integer NOT NULL, `input_data` varchar(512) NOT NULL, `output_data` numeric(7, 4) NOT NULL, `prediction_date` datetime NOT NULL, `predicted_on_date` date NOT NULL, `prediction_is_automate` varchar(1) NOT NULL, `neiro_net_id` integer NOT NULL);
--
-- Create model Quotes
--
CREATE TABLE `prediction_research_quotes` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `quote_date` date NOT NULL, `quote_value` numeric(8, 4) NOT NULL, `quote_type` varchar(10) NOT NULL, `creation_date` datetime NOT NULL);
--
-- Create model Training
--
CREATE TABLE `prediction_research_training` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `training_data_file` varchar(512) NOT NULL, `training_start_time` datetime NOT NULL, `training_end_time` datetime NULL, `neiro_net_id` integer NOT NULL);
--
-- Create model TrainingResult
--
CREATE TABLE `prediction_research_trainingresult` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `training_epochs` integer NOT NULL, `errors` numeric(9, 6) NOT NULL, `training_id` integer NOT NULL);

ALTER TABLE `prediction_research_prediction` ADD CONSTRAINT `predict_neiro_net_id_6b3d20d6_fk_prediction_research_neironet_id` FOREIGN KEY (`neiro_net_id`) REFERENCES `prediction_research_neironet` (`id`);
ALTER TABLE `prediction_research_training` ADD CONSTRAINT `predict_neiro_net_id_1f560ce8_fk_prediction_research_neironet_id` FOREIGN KEY (`neiro_net_id`) REFERENCES `prediction_research_neironet` (`id`);
ALTER TABLE `prediction_research_trainingresult` ADD CONSTRAINT `predicti_training_id_532704bb_fk_prediction_research_training_id` FOREIGN KEY (`training_id`) REFERENCES `prediction_research_training` (`id`);

COMMIT;