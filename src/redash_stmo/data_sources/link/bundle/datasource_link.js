/* eslint-disable no-console, camelcase */
import React from 'react';
import PropTypes from 'prop-types';
import { react2angular } from 'react2angular';

class DatasourceLink extends React.Component {
  static propTypes = {
    clientConfig: PropTypes.object.isRequired,
    datasourceId: PropTypes.number.isRequired,
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
    if (this.props.datasourceId !== prevProps.datasourceId) {
      this.loadURLData();
    }
  }

  loadURLData() {
    fetch(`${this.props.clientConfig.basePath}api/data_sources/${this.props.datasourceId}/link`)
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

export default function init(ngModule) {
  ngModule.component('datasourceLink', react2angular(DatasourceLink, ['datasourceId'], ['clientConfig']));
}

init.init = true;
