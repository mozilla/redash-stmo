/* eslint-disable camelcase */
import React from 'react';
import { render } from 'react-dom';
import { debounce } from 'lodash';

function getValidateQuery($http, dataSourceId, query) {
  return $http.post(`api/data_sources/${dataSourceId}/validate`, { query });
}

class DataSourceValidator extends React.Component {
  constructor(props) {
    super(props);
    this.getValidateQuery = debounce(getValidateQuery, 500);
    this.state = {
      valid: false,
      report: '',
    };
  }

  componentDidMount() {
    this.componentDidUpdate();
  }

  componentDidUpdate(prevProps, prevState) {
    const queryTextChanged = !prevProps || prevProps.queryText !== this.props.queryText;
    const reportChanged = prevState && prevState.report !== this.state.report;
    if (queryTextChanged || reportChanged) {
      const p = this.getValidateQuery(this.props.$http, this.props.dataSourceId, this.props.queryText);
      if (p) {
        p.then((response) => { this.setState(response.data); });
      }
    }
  }

  render() {
    return (
      <React.Fragment>
        <i className={`zmdi zmdi-${this.state.valid ? 'check' : 'minus'}-circle`} /> {this.state.report}
      </React.Fragment>
    );
  }
}

export default function init(ngModule) {
  ngModule.decorator('queryEditorDirective', ['$delegate', '$http', ($delegate, $http) => {
    const controller = $delegate[0].controller;
    const controllerFunc = controller[controller.length - 1];
    controllerFunc.prototype.origRender = controllerFunc.prototype.render;

    controllerFunc.prototype.render = function newRender() {
      this.origRender();
      const container = document.querySelector('.editor__control div');
      let status = document.querySelector('#stmo_datasource_validator');
      if (!status) {
        status = document.createElement('div');
        status.id = 'stmo_datasource_validator';
      } else {
        container.removeChild(status);
      }
      container.appendChild(status);
      render(
        <DataSourceValidator queryText={this.props.queryText} dataSourceId={this.dataSource.id} $http={$http} />,
        status,
      );
    };
    return $delegate;
  }]);
}

init.init = true;
