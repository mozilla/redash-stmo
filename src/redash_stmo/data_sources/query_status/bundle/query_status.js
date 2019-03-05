/* eslint-disable camelcase */
import React from 'react';
import { render } from 'react-dom';
import { debounce } from 'lodash';

function getQueryStatus($http, query, data_source_id) {
  return $http.post('api/queries/check', { query, data_source_id });
}

class QueryStatus extends React.Component {
  constructor(props) {
    super(props);
    this.getQueryStatus = debounce(getQueryStatus, 500);
    this.state = {
      valid: false,
      report: '',
    };
  }
  componentDidMount() {
    this.componentDidUpdate();
  }

  componentDidUpdate(prevProps, prevState) {
    if (!prevProps || prevProps.queryText !== this.props.queryText || (prevState && prevState.report !== this.state.report)) {
      const p = this.getQueryStatus(this.props.$http, this.props.queryText, this.props.dataSourceId);
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
      let status = document.querySelector('#stmo_query_status');
      if (!status) {
        status = document.createElement('div');
        status.id = 'stmo_query_status';
        container.appendChild(status);
      }
      render(
          <QueryStatus queryText={this.props.queryText} dataSourceId={this.dataSource.id} $http={$http} />,
        status,
      );
    };
    return $delegate;
  }]);
}

init.init = true;
