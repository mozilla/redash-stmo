/* eslint-disable no-console, camelcase */
import React from 'react';
import PropTypes from 'prop-types';
import { clientConfig } from "@/services/auth";

export default class DataSourceLink extends React.Component {
  static propTypes = {
    dataSourceId: PropTypes.number.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = {
      type_name: '',
      doc_url: '',
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
    fetch(`${clientConfig.basePath}api/data_sources/${this.props.dataSourceId}/link`)
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
        const { type_name, doc_url } = json.message;
        this.setState({ type_name, doc_url });
      });
  }

  render() {
    if (!this.state.doc_url) {
      return null;
    }
    return (
      <span>
        <a href={this.state.doc_url}> {this.state.type_name} documentation</a>
      </span>
    );
  }
}
