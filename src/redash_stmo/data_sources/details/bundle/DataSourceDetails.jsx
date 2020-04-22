/* eslint-disable no-console, camelcase */
import React from 'react';
import PropTypes from 'prop-types';
import { clientConfig } from "@/services/auth";
import registerComponent from "@/components/DynamicComponent";


export default class DataSourceDetails extends React.Component {
  static propTypes = {
    dataSourceId: PropTypes.number.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = {
      type_name: '',
      doc_url: '',
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
    fetch(`${clientConfig.basePath}api/data_sources/${this.props.dataSourceId}/details`)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        }
        return {};
      })
      .catch((error) => {
        console.error(`Error loading data source URL: ${error}`);
        return {};
      })
      .then((json) => {
        const { type_name, doc_url, version } = json.message;
        this.setState({ type_name, doc_url, version });
      });
  }

  render() {
    return (
      <span>
        {this.state.type_name} {this.state.version && <span>, version: {this.state.version}</span>}
        {this.state.doc_url && <span>, <a href={this.state.doc_url}>docs</a></span>}
      </span>
    );
  }
}

registerComponent("SelectDataSourceExtra", DataSourceDetails)
