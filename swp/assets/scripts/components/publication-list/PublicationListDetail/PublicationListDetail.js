import _ from 'utils/i18n';

import Page from 'components/Page';
import PublicationList from 'components/publication/PublicationList';

import EditableTitle from './EditableTitle';
import ExportButton from './ExportButton';
import DeleteButton from './DeleteButton';

const EmptyMessage = _('This publication list is empty.');

const PublicationListDetail = ({id, name, publications}) => {
    const title = <EditableTitle id={id} title={name} />;
    const isEmpty = publications.length === 0;
    const actions = [
        isEmpty || <ExportButton key="export" id={id} />,
        <DeleteButton key="delete" id={id} name={name} />,
    ];

    return (
        <Page title={title} actions={actions}>
            <div className="mt-4">
                {isEmpty || <PublicationList items={publications} showMenu />}
                {isEmpty && <p>{EmptyMessage}</p>}
            </div>
        </Page>
    );
};

export default PublicationListDetail;
