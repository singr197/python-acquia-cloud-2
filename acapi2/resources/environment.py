#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manipulate environments and perform related actions."""

from acapi2.resources.acquiaresource import AcquiaResource
from requests.sessions import Session


class Environment(AcquiaResource):

    def code_switch(self, branch_tag: str) -> Session:
        """
        Switch code on this environment to a different branch or release tag.

        :param branch_tag: The tag to switch to.
        """
        uri = f"{self.uri}/code/actions/switch"
        data = {
            "branch": branch_tag
        }

        response = self.request(uri=uri, method="POST", data=data)
        return response

    def configure(self, data: dict) -> Session:
        """
        Modify configuration settings for an environment.

        :param data: Configuration parameters.
        """
        return self.request(uri=self.uri, method="PUT", data=data)

    def create_domain(self, domain: str) -> Session:
        """
        Add a domain to the environment.

        :param domain: Domain to add to the environment.
        """
        uri = f"{self.uri}/domains"
        data = {
            "hostname": domain
        }
        response = self.request(uri=uri, method="POST", data=data)

        return response

    def create_log_forwarding_destinations(
        self,
        label: str,
        sources: list,
        consumer: str,
        credentials: dict,
        address: str
    ) -> Session:
        """
        Create a log forwarding destination.
        """
        uri = f"{self.uri}/log-forwarding-destinations"
        data = {
            "label": label,
            "sources": sources,
            "consumer": consumer,
            "credentials": credentials,
            "address": address
        }
        response = self.request(uri=uri, method="POST", data=data)

        return response

    def delete_domain(self, domain: str) -> Session:
        """
        Remove the domain from the environment.

        :param domain: Domain name to delete.
        """
        uri = f"{self.uri}/domains/{domain}"
        response = self.request(uri=uri, method="DELETE")

        return response

    def clear_varnish_domain(self, domain: str) -> Session:
        """
        Clear the Varnish cache for the domain attached to this environment.

        :param domain: Domain name.
        """
        uri = f"{self.uri}/domains/{domain}/actions/clear-varnish"
        data = {
            "hostname": domain
        }
        response = self.request(uri=uri, method="POST", data=data)

        return response

    def clear_varnish_domains(self, domains: list) -> Session:
        """
        Clear the Varnish cache for multiple domains
         attached to this environment.

        :param domains: Domain name list.
        """
        uri = f"{self.uri}/domains/actions/clear-varnish"
        data = {
            "domains": domains
        }

        response = self.request(uri=uri, method="POST", data=data)

        return response

    def destroy(self):
        """
        Delete a CD environment.
        """
        response = self.request(uri=self.uri, method="DELETE")

        return response

    def deploy_code(self, id_from: str) -> Session:
        """
        Deploy code to this environment.

        :param id_from: uuid for the environment to deploy code from.
        """
        uri = f"{self.uri}/code"
        data = {
            "source": id_from
        }

        response = self.request(uri=uri, method="POST", data=data)
        return response

    def deploy_database(self, id_from: str, db_name: str) -> None:
        """
        Copy a database to this environment.

        :param id_from: uuid for the environment to deploy the db from.
        :param db_name: the database name to use.
        """
        uri = f"{self.uri}/databases"
        data = {
            "name": db_name,
            "source": id_from
        }

        response = self.request(uri=uri, method="POST", data=data)
        return response

    def deploy_files(self, id_from: str) -> Session:
        """
        Copy files to this environment.

        :param id_from: uuid for the environment to deploy the files from.
        """
        uri = f"{self.uri}/files"
        data = {
            "source": id_from
        }

        response = self.request(uri=uri, method="POST", data=data)
        return response

    def get_crons(self) -> dict:
        """
        Return a list of the cron jobs on an environment.
        """
        uri = f"{self.uri}/crons"

        response = self.request(uri=uri)
        return response.json()

    def get_log_forwarding_destinations(self) -> dict:
        """
        Return a collection of log forwarding destinations.
        """
        uri = f"{self.uri}/log-forwarding-destinations"

        response = self.request(uri=uri)
        return response.json()

    def get_servers(self) -> dict:
        """
        Return a list of servers.
        """
        uri = f"{self.uri}/servers"

        response = self.request(uri=uri)
        return response.json()

    def get_php_version(self) -> dict:
        """
        Get the PHP version number.
        """
        uri = f"{self.uri}/"

        response = self.request(uri=uri)
        env_config = response.json()
        return {'php_version': env_config['configuration']['php']['version']}

    def set_php_version(self, version: str) -> Session:
        """
        Set the PHP version.

        :param version: PHP version number to use.
        """
        data = {
            "version": version
        }

        return self.configure(data)
