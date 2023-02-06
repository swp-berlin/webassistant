import _ from 'utils/i18n';

import Page from 'components/Page';
import PublicationList from 'components/publication/PublicationList';
import PublicationListMenu from 'components/PublicationListMenu';

import EditableTitle from './EditableTitle';
import ExportButton from './ExportButton';
import DeleteButton from './DeleteButton';
import PublicationRemoveButton from './PublicationRemoveButton';

const EmptyMessage = _('This publication list is empty.');

const PublicationListDetail = ({publicationList}) => {
    const {id, name, publications} = publicationList;
    const title = <EditableTitle id={id} title={name} />;
    const isEmpty = publications.length === 0;
    const actions = [
        isEmpty || <ExportButton key="export" id={id} />,
        <DeleteButton key="delete" id={id} name={name} />,
    ];

    return (
        <Page title={title} actions={actions}>
            <div className="mt-4">
                {isEmpty && <p>{EmptyMessage}</p>}
                {isEmpty || (
                    <PublicationList items={publications}>
                        <PublicationListMenu>
                            <PublicationRemoveButton publicationList={publicationList} />
                        </PublicationListMenu>
                    </PublicationList>
                )}
            </div>
        </Page>
    );
};

export default PublicationListDetail;
