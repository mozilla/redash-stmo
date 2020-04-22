/* eslint-disable no-console, camelcase */
import React from 'react';
import PropTypes from 'prop-types';
import { clientConfig } from "@/services/auth";

export default class DataSourceVersion extends React.Component {
  static propTypes = {
    dataSourceId: PropTypes.number.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = {
      version: '',
    };
  }

  componentDidMount() {
    this.loadURLData();
  }

  componentDidUpdate(prevProps) {
    if (this.props.dataSourceId !== prevProps.dataSourceId) {
      this.loadURLData();
    }
  }

  loadURLData() {
    fetch(`${clientConfig.basePath}api/data_sources/${this.props.dataSourceId}/version`)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        }
        return {};
      })
      .catch((error) => {
        console.error(`Error loading data source version: ${error}`);
        return {};
      })
      .then((json) => {
        this.setState({ version: json.version });
      });
  }

  render() {
    if (!this.state.version) {
      return null;
    }
    return (
      <span>{this.state.version}</span>
    );
  }
}
