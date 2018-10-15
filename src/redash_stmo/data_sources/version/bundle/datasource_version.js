import React from 'react';
import PropTypes from 'prop-types';
import { react2angular } from 'react2angular';

class DatasourceVersion extends React.Component {
  static propTypes = {
    clientConfig: PropTypes.object.isRequired,
    datasourceId: PropTypes.number.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = {
      version: '',
    };
  }

  loadURLData() {
    fetch(`${this.props.clientConfig.basePath}api/data_sources/${this.props.datasourceId}/version`)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        }
        return {};
      })
      .catch(error => {
        console.error(`Error loading data source version: ${error}`);
        return {};
      })
      .then((json) => {
        this.setState({ version: json.version });
      });
  }

  componentDidMount() {
    this.loadURLData();
  }

  componentDidUpdate(prevProps) {
    if (this.props.datasourceId !== prevProps.datasourceId) {
      this.loadURLData();
    }
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

export default function init(ngModule) {
  ngModule.component('datasourceVersion', react2angular(DatasourceVersion, ['datasourceId'], ['clientConfig']));
}
