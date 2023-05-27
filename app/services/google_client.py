from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings


DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'


SHEET_BODY = {
    'properties': {'sheetId': 0,
                   'title': settings.report_title,
                   'sheetType': 'GRID',
                   'gridProperties': {'rowCount': 100,
                                      'columnCount': 10}}
}

SPREADSHEET_BODY = {
    'properties': {
        'title': settings.report_title,
        'locale': 'ru_RU'},
    'sheets': [SHEET_BODY]
}

USER_PERMISSON_BODY = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': settings.email}


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle
) -> None:
    """Выдача прав доступа личному гугл-аккаунту к документу."""
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=USER_PERMISSON_BODY,
            fields='id'
        ))


async def spreadsheets_create(
        wrapper_service: Aiogoogle
) -> str:
    """Создание гугл-таблицы."""
    service = await wrapper_service.discover(
        'sheets', settings.google_sheets_api_version)
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    return response['spreadsheetId']


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Формирование отчета в гугл-таблице на основе переданных данных."""
    service = await wrapper_services.discover(
        'sheets', settings.google_sheets_api_version)
    table_values = [
        ['Отчет от', datetime.now().strftime(DATETIME_FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = list(project)
        new_row[1] = str(timedelta(days=project[1]))
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=settings.report_range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_spreadsheets_from_disk(
        spreadsheet_title: str,
        wrapper_service: Aiogoogle
) -> list[dict[str, str]]:
    """Получить список всех сформированных отчетов."""
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    spreadsheets = await wrapper_service.as_service_account(
        service.files.list(
            q=f'mimeType="application/vnd.google-apps.spreadsheet" and \
            name="{spreadsheet_title}"')
    )
    return spreadsheets['files']


async def delete_spreadsheets_from_disk(
        wrapper_service: Aiogoogle
) -> None:
    """Удалить все отчеты с диска."""
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    spreadsheets = await get_spreadsheets_from_disk(settings.report_title,
                                                    wrapper_service)
    for spreadsheet in spreadsheets:
        await wrapper_service.as_service_account(
            service.files.delete(fileId=spreadsheet['id']))
