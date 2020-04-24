/* eslint-disable no-console, camelcase */
import React from 'react';
import PropTypes from 'prop-types';
import { clientConfig } from "@/services/auth";
import { registerComponent } from "@/components/DynamicComponent";


export default class DataSourceDetails extends React.Component {
  static propTypes = {
    dataSourceId: PropTypes.number,
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
    if (this.props.dataSourceId) {
      this.loadURLData();
    }
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
      <div className="m-t-5">
        {this.state.type_name &&
          <span>Data source type: {this.state.doc_url &&
            <a href={this.state.doc_url}>{this.state.type_name}</a> ||
            <span>{this.state.type_name}</span>
          }
          </span>
        }
        {this.state.version && <span>({this.state.version})</span>}
      </div>
    );
  }
}

registerComponent("SelectDataSourceExtra", DataSourceDetails)
